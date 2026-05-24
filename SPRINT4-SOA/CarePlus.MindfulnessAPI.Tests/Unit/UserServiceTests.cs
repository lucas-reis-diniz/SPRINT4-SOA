using CarePlus.MindfulnessAPI.Mapping;
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
