using CarePlus.MindfulnessAPI.Mapping.Interfaces;
using CarePlus.MindfulnessAPI.Models.DTOs;
using CarePlus.MindfulnessAPI.Models.Entities;
using CarePlus.MindfulnessAPI.Repositories.Interfaces;
using CarePlus.MindfulnessAPI.Security.Interfaces;
using CarePlus.MindfulnessAPI.Services.Interfaces;

namespace CarePlus.MindfulnessAPI.Services;

public class UserService : IUserService
{
    private readonly IUserRepository _repository;
    private readonly IPasswordHasherService _passwordHasher;
    private readonly IPasswordPolicy _passwordPolicy;
    private readonly IModelMapper<User, UserResponseDTO> _mapper;

    public UserService(
        IUserRepository repository,
        IPasswordHasherService passwordHasher,
        IPasswordPolicy passwordPolicy,
        IModelMapper<User, UserResponseDTO> mapper)
    {
        _repository = repository;
        _passwordHasher = passwordHasher;
        _passwordPolicy = passwordPolicy;
        _mapper = mapper;
    }

    public async Task<IEnumerable<UserResponseDTO>> GetAllAsync()
    {
        var users = await _repository.GetAllAsync();
        return users.Select(_mapper.Map);
    }

    public async Task<UserResponseDTO?> GetByIdAsync(Guid id)
    {
        var user = await _repository.GetByIdAsync(id);
        return user == null ? null : _mapper.Map(user);
    }

    public async Task<UserResponseDTO> CreateAsync(UserCreateDTO dto)
    {
        _passwordPolicy.Validate(dto.Senha);

        var normalizedEmail = dto.Email.Trim().ToLowerInvariant();
        var existingUser = await _repository.GetByEmailAsync(normalizedEmail);
        if (existingUser != null)
            throw new InvalidOperationException($"Já existe um usuário com o email '{dto.Email}'.");

        var user = new User
        {
            Nome = dto.Nome.Trim(),
            Email = normalizedEmail,
            PasswordHash = _passwordHasher.Hash(dto.Senha),
            DataNascimento = dto.DataNascimento,
            Role = dto.Role
        };

        var created = await _repository.CreateAsync(user);
        return _mapper.Map(created);
    }

    public async Task<UserResponseDTO?> UpdateAsync(Guid id, UserUpdateDTO dto)
    {
        var user = await _repository.GetByIdAsync(id);
        if (user == null) return null;

        var normalizedEmail = dto.Email.Trim().ToLowerInvariant();
        var existingUser = await _repository.GetByEmailAsync(normalizedEmail);
        if (existingUser != null && existingUser.Id != id)
            throw new InvalidOperationException($"Já existe outro usuário com o email '{dto.Email}'.");

        user.Nome = dto.Nome.Trim();
        user.Email = normalizedEmail;
        user.DataNascimento = dto.DataNascimento;
        user.Role = dto.Role;

        var updated = await _repository.UpdateAsync(user);
        return _mapper.Map(updated);
    }

    public async Task<bool> DeleteAsync(Guid id)
    {
        return await _repository.DeleteAsync(id);
    }
}
