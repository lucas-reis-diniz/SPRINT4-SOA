from pathlib import Path
root = Path('/home/ubuntu/SPRINT3-SOA')

def write(relative, content):
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')

unit = root / 'CarePlus.MindfulnessAPI.Tests/UnitTest1.cs'
if unit.exists():
    unit.unlink()

write('CarePlus.MindfulnessAPI.Tests/Unit/DefaultPasswordPolicyTests.cs', r'''using CarePlus.MindfulnessAPI.Security;

namespace CarePlus.MindfulnessAPI.Tests.Unit;

public class DefaultPasswordPolicyTests
{
    [Fact]
    public void Validate_WhenPasswordHasLettersAndNumbers_ShouldNotThrow()
    {
        var policy = new DefaultPasswordPolicy();

        var exception = Record.Exception(() => policy.Validate("Senha123"));

        Assert.Null(exception);
    }

    [Theory]
    [InlineData("")]
    [InlineData("1234567")]
    [InlineData("somenteletras")]
    public void Validate_WhenPasswordDoesNotMatchPolicy_ShouldThrow(string password)
    {
        var policy = new DefaultPasswordPolicy();

        Assert.Throws<InvalidOperationException>(() => policy.Validate(password));
    }
}
''')

write('CarePlus.MindfulnessAPI.Tests/Unit/BCryptPasswordHasherServiceTests.cs', r'''using CarePlus.MindfulnessAPI.Security;

namespace CarePlus.MindfulnessAPI.Tests.Unit;

public class BCryptPasswordHasherServiceTests
{
    [Fact]
    public void Hash_ShouldCreateNonPlainTextHash_AndVerifyOriginalPassword()
    {
        var hasher = new BCryptPasswordHasherService();
        const string password = "Senha123";

        var hash = hasher.Hash(password);

        Assert.NotEqual(password, hash);
        Assert.True(hasher.Verify(password, hash));
        Assert.False(hasher.Verify("SenhaErrada123", hash));
    }
}
''')

write('CarePlus.MindfulnessAPI.Tests/Unit/UserServiceTests.cs', r'''using CarePlus.MindfulnessAPI.Mapping;
using CarePlus.MindfulnessAPI.Models.DTOs;
using CarePlus.MindfulnessAPI.Models.Entities;
using CarePlus.MindfulnessAPI.Models.Enums;
using CarePlus.MindfulnessAPI.Repositories.Interfaces;
using CarePlus.MindfulnessAPI.Security;
using CarePlus.MindfulnessAPI.Security.Interfaces;
using CarePlus.MindfulnessAPI.Services;
using Moq;

namespace CarePlus.MindfulnessAPI.Tests.Unit;

public class UserServiceTests
{
    [Fact]
    public async Task CreateAsync_WhenEmailAlreadyExists_ShouldThrowInvalidOperationException()
    {
        var repository = new Mock<IUserRepository>();
        repository.Setup(r => r.GetByEmailAsync("maria@teste.com"))
            .ReturnsAsync(new User { Id = Guid.NewGuid(), Nome = "Maria", Email = "maria@teste.com" });

        var service = BuildService(repository.Object);
        var dto = new UserCreateDTO("Maria", "maria@teste.com", "Senha123", null, UserRole.User);

        await Assert.ThrowsAsync<InvalidOperationException>(() => service.CreateAsync(dto));
    }

    [Fact]
    public async Task CreateAsync_WhenValidData_ShouldHashPasswordAndReturnUserResponse()
    {
        User? persistedUser = null;
        var repository = new Mock<IUserRepository>();
        repository.Setup(r => r.GetByEmailAsync("joao@teste.com"))
            .ReturnsAsync((User?)null);
        repository.Setup(r => r.CreateAsync(It.IsAny<User>()))
            .ReturnsAsync((User user) =>
            {
                persistedUser = user;
                user.Id = Guid.NewGuid();
                return user;
            });

        var service = BuildService(repository.Object);
        var dto = new UserCreateDTO("João", "joao@teste.com", "Senha123", null, UserRole.Admin);

        var result = await service.CreateAsync(dto);

        Assert.NotNull(persistedUser);
        Assert.Equal("João", result.Nome);
        Assert.Equal("joao@teste.com", result.Email);
        Assert.Equal(UserRole.Admin, result.Role);
        Assert.NotEqual("Senha123", persistedUser!.PasswordHash);
    }

    private static UserService BuildService(IUserRepository repository)
    {
        IPasswordHasherService hasher = new BCryptPasswordHasherService();
        return new UserService(repository, hasher, new DefaultPasswordPolicy(), new UserMapper());
    }
}
''')

write('CarePlus.MindfulnessAPI.Tests/Integration/CustomWebApplicationFactory.cs', r'''using CarePlus.MindfulnessAPI.Data;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Mvc.Testing;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.DependencyInjection.Extensions;

namespace CarePlus.MindfulnessAPI.Tests.Integration;

public class CustomWebApplicationFactory : WebApplicationFactory<Program>
{
    protected override void ConfigureWebHost(IWebHostBuilder builder)
    {
        builder.UseEnvironment("Development");

        builder.ConfigureServices(services =>
        {
            services.RemoveAll<DbContextOptions<AppDbContext>>();
            services.AddDbContext<AppDbContext>(options =>
                options.UseInMemoryDatabase($"CarePlusMindfulnessTests_{Guid.NewGuid()}"));

            using var scope = services.BuildServiceProvider().CreateScope();
            var context = scope.ServiceProvider.GetRequiredService<AppDbContext>();
            context.Database.EnsureDeleted();
            context.Database.EnsureCreated();
        });
    }
}
''')

write('CarePlus.MindfulnessAPI.Tests/Integration/AuthAndAuthorizationIntegrationTests.cs', r'''using System.Net;
using System.Net.Http.Headers;
using System.Net.Http.Json;
using CarePlus.MindfulnessAPI.Models.DTOs;

namespace CarePlus.MindfulnessAPI.Tests.Integration;

public class AuthAndAuthorizationIntegrationTests : IClassFixture<CustomWebApplicationFactory>
{
    private readonly HttpClient _client;

    public AuthAndAuthorizationIntegrationTests(CustomWebApplicationFactory factory)
    {
        _client = factory.CreateClient();
    }

    [Fact]
    public async Task PublicEndpoint_WhenAnonymous_ShouldReturnOk()
    {
        var response = await _client.GetAsync("/api/WellnessContents/active");

        Assert.Equal(HttpStatusCode.OK, response.StatusCode);
    }

    [Fact]
    public async Task ProtectedAdminEndpoint_WhenAnonymous_ShouldReturnUnauthorized()
    {
        var response = await _client.GetAsync("/api/Users");

        Assert.Equal(HttpStatusCode.Unauthorized, response.StatusCode);
    }

    [Fact]
    public async Task Register_WhenValidUser_ShouldReturnJwtToken()
    {
        var request = new RegisterRequestDTO("Ana Teste", $"ana.{Guid.NewGuid():N}@teste.com", "Senha123", null);

        var response = await _client.PostAsJsonAsync("/api/Auth/register", request);
        var body = await response.Content.ReadFromJsonAsync<ApiResponse<AuthResponseDTO>>();

        Assert.Equal(HttpStatusCode.Created, response.StatusCode);
        Assert.NotNull(body?.Dados);
        Assert.False(string.IsNullOrWhiteSpace(body!.Dados!.Token));
        Assert.Equal("Ana Teste", body.Dados.Usuario.Nome);
    }

    [Fact]
    public async Task AuthenticatedEndpoint_WhenUsingJwt_ShouldReturnOk()
    {
        var request = new RegisterRequestDTO("Carlos Teste", $"carlos.{Guid.NewGuid():N}@teste.com", "Senha123", null);
        var loginResponse = await _client.PostAsJsonAsync("/api/Auth/register", request);
        var loginBody = await loginResponse.Content.ReadFromJsonAsync<ApiResponse<AuthResponseDTO>>();

        _client.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", loginBody!.Dados!.Token);
        var response = await _client.GetAsync("/api/MeditationSessions");

        Assert.Equal(HttpStatusCode.OK, response.StatusCode);
    }
}
''')

print('Testes da Sprint 4 criados.')
