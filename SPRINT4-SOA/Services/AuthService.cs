using CarePlus.MindfulnessAPI.Mapping.Interfaces;
using CarePlus.MindfulnessAPI.Models.DTOs;
using CarePlus.MindfulnessAPI.Models.Entities;
using CarePlus.MindfulnessAPI.Models.Enums;
using CarePlus.MindfulnessAPI.Repositories.Interfaces;
using CarePlus.MindfulnessAPI.Security.Interfaces;
using CarePlus.MindfulnessAPI.Services.Interfaces;

namespace CarePlus.MindfulnessAPI.Services;

public class AuthService : IAuthService
{
    private readonly IUserRepository _userRepository;
    private readonly IPasswordHasherService _passwordHasher;
    private readonly IPasswordPolicy _passwordPolicy;
    private readonly IJwtTokenService _jwtTokenService;
    private readonly IModelMapper<User, UserResponseDTO> _userMapper;

    public AuthService(
        IUserRepository userRepository,
        IPasswordHasherService passwordHasher,
        IPasswordPolicy passwordPolicy,
        IJwtTokenService jwtTokenService,
        IModelMapper<User, UserResponseDTO> userMapper)
    {
        _userRepository = userRepository;
        _passwordHasher = passwordHasher;
        _passwordPolicy = passwordPolicy;
        _jwtTokenService = jwtTokenService;
        _userMapper = userMapper;
    }

    public async Task<AuthResponseDTO> RegisterAsync(RegisterRequestDTO dto)
    {
        _passwordPolicy.Validate(dto.Senha);

        var normalizedEmail = dto.Email.Trim().ToLowerInvariant();
        var existingUser = await _userRepository.GetByEmailAsync(normalizedEmail);
        if (existingUser != null)
            throw new InvalidOperationException($"Já existe um usuário com o email '{dto.Email}'.");

        var user = new User
        {
            Nome = dto.Nome.Trim(),
            Email = normalizedEmail,
            PasswordHash = _passwordHasher.Hash(dto.Senha),
            DataNascimento = dto.DataNascimento,
            Role = UserRole.User
        };

        var created = await _userRepository.CreateAsync(user);
        return CreateAuthResponse(created);
    }

    public async Task<AuthResponseDTO> LoginAsync(LoginRequestDTO dto)
    {
        var user = await _userRepository.GetByEmailAsync(dto.Email.Trim().ToLowerInvariant());
        if (user == null || !_passwordHasher.Verify(dto.Senha, user.PasswordHash))
            throw new UnauthorizedAccessException("E-mail ou senha inválidos.");

        return CreateAuthResponse(user);
    }

    private AuthResponseDTO CreateAuthResponse(User user)
    {
        var token = _jwtTokenService.GenerateToken(user);
        return new AuthResponseDTO(token.Token, token.ExpiresAt, _userMapper.Map(user));
    }
}
