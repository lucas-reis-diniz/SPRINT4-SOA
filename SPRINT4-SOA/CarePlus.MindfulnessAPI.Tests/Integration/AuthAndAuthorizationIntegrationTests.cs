using System.Net;
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
