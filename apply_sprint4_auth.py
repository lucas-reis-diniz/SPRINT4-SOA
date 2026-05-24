from pathlib import Path

root = Path('/home/ubuntu/SPRINT3-SOA')
hash_value = '$2b$11$FbIkP7XIZUKs/00gs6Z0yOswD4wiCZSjIIOktQh6VVx4VE5a9j/vu'

def write(relative, content):
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')

# Corrige hash BCrypt seedado para a senha CarePlus@123.
ctx = (root / 'Data/AppDbContext.cs').read_text(encoding='utf-8')
ctx = ctx.replace('$2a$11$H5NZa1PQUCByewMgbzxDxOih5WxUxMtZKsk/1K4uFTIB5B2dG78Hu', hash_value)
(root / 'Data/AppDbContext.cs').write_text(ctx, encoding='utf-8')

write('Security/Interfaces/IPasswordHasherService.cs', r'''namespace CarePlus.MindfulnessAPI.Security.Interfaces;

public interface IPasswordHasherService
{
    string Hash(string password);
    bool Verify(string password, string passwordHash);
}
''')

write('Security/Interfaces/IJwtTokenService.cs', r'''using CarePlus.MindfulnessAPI.Models.Entities;

namespace CarePlus.MindfulnessAPI.Security.Interfaces;

public interface IJwtTokenService
{
    (string Token, DateTime ExpiresAt) GenerateToken(User user);
}
''')

write('Security/BCryptPasswordHasherService.cs', r'''using CarePlus.MindfulnessAPI.Security.Interfaces;

namespace CarePlus.MindfulnessAPI.Security;

public class BCryptPasswordHasherService : IPasswordHasherService
{
    private const int WorkFactor = 11;

    public string Hash(string password)
    {
        if (string.IsNullOrWhiteSpace(password))
            throw new InvalidOperationException("A senha é obrigatória.");

        return BCrypt.Net.BCrypt.HashPassword(password, WorkFactor);
    }

    public bool Verify(string password, string passwordHash)
    {
        if (string.IsNullOrWhiteSpace(password) || string.IsNullOrWhiteSpace(passwordHash))
            return false;

        return BCrypt.Net.BCrypt.Verify(password, passwordHash);
    }
}
''')

write('Security/JwtTokenService.cs', r'''using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using System.Text;
using CarePlus.MindfulnessAPI.Models.Entities;
using CarePlus.MindfulnessAPI.Security.Interfaces;
using Microsoft.IdentityModel.Tokens;

namespace CarePlus.MindfulnessAPI.Security;

public class JwtTokenService : IJwtTokenService
{
    private readonly IConfiguration _configuration;

    public JwtTokenService(IConfiguration configuration)
    {
        _configuration = configuration;
    }

    public (string Token, DateTime ExpiresAt) GenerateToken(User user)
    {
        var issuer = _configuration["Jwt:Issuer"] ?? throw new InvalidOperationException("Jwt:Issuer não configurado.");
        var audience = _configuration["Jwt:Audience"] ?? throw new InvalidOperationException("Jwt:Audience não configurado.");
        var key = _configuration["Jwt:Key"] ?? throw new InvalidOperationException("Jwt:Key não configurado.");
        var expirationMinutes = int.TryParse(_configuration["Jwt:ExpirationMinutes"], out var minutes) ? minutes : 120;

        var claims = new List<Claim>
        {
            new(JwtRegisteredClaimNames.Sub, user.Id.ToString()),
            new(JwtRegisteredClaimNames.Email, user.Email),
            new(ClaimTypes.NameIdentifier, user.Id.ToString()),
            new(ClaimTypes.Name, user.Nome),
            new(ClaimTypes.Email, user.Email),
            new(ClaimTypes.Role, user.Role.ToString())
        };

        var securityKey = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(key));
        var credentials = new SigningCredentials(securityKey, SecurityAlgorithms.HmacSha256);
        var expiresAt = DateTime.UtcNow.AddMinutes(expirationMinutes);

        var token = new JwtSecurityToken(
            issuer: issuer,
            audience: audience,
            claims: claims,
            expires: expiresAt,
            signingCredentials: credentials
        );

        return (new JwtSecurityTokenHandler().WriteToken(token), expiresAt);
    }
}
''')

write('Services/AuthService.cs', r'''using CarePlus.MindfulnessAPI.Models.DTOs;
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
    private readonly IJwtTokenService _jwtTokenService;

    public AuthService(
        IUserRepository userRepository,
        IPasswordHasherService passwordHasher,
        IJwtTokenService jwtTokenService)
    {
        _userRepository = userRepository;
        _passwordHasher = passwordHasher;
        _jwtTokenService = jwtTokenService;
    }

    public async Task<AuthResponseDTO> RegisterAsync(RegisterRequestDTO dto)
    {
        ValidatePassword(dto.Senha);

        var existingUser = await _userRepository.GetByEmailAsync(dto.Email);
        if (existingUser != null)
            throw new InvalidOperationException($"Já existe um usuário com o email '{dto.Email}'.");

        var user = new User
        {
            Nome = dto.Nome.Trim(),
            Email = dto.Email.Trim().ToLowerInvariant(),
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
        var userDto = new UserResponseDTO(
            user.Id,
            user.Nome,
            user.Email,
            user.DataNascimento,
            user.Role,
            user.CriadoEm,
            user.Sessions?.Count ?? 0,
            user.MoodEntries?.Count ?? 0
        );

        return new AuthResponseDTO(token.Token, token.ExpiresAt, userDto);
    }

    private static void ValidatePassword(string password)
    {
        if (string.IsNullOrWhiteSpace(password) || password.Length < 8)
            throw new InvalidOperationException("A senha deve possuir pelo menos 8 caracteres.");
    }
}
''')

write('Services/UserService.cs', r'''using CarePlus.MindfulnessAPI.Models.DTOs;
using CarePlus.MindfulnessAPI.Models.Entities;
using CarePlus.MindfulnessAPI.Repositories.Interfaces;
using CarePlus.MindfulnessAPI.Security.Interfaces;
using CarePlus.MindfulnessAPI.Services.Interfaces;

namespace CarePlus.MindfulnessAPI.Services;

public class UserService : IUserService
{
    private readonly IUserRepository _repository;
    private readonly IPasswordHasherService _passwordHasher;

    public UserService(IUserRepository repository, IPasswordHasherService passwordHasher)
    {
        _repository = repository;
        _passwordHasher = passwordHasher;
    }

    public async Task<IEnumerable<UserResponseDTO>> GetAllAsync()
    {
        var users = await _repository.GetAllAsync();
        return users.Select(MapToDTO);
    }

    public async Task<UserResponseDTO?> GetByIdAsync(Guid id)
    {
        var user = await _repository.GetByIdAsync(id);
        return user == null ? null : MapToDTO(user);
    }

    public async Task<UserResponseDTO> CreateAsync(UserCreateDTO dto)
    {
        ValidatePassword(dto.Senha);

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
        return MapToDTO(created);
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
        return MapToDTO(updated);
    }

    public async Task<bool> DeleteAsync(Guid id)
    {
        return await _repository.DeleteAsync(id);
    }

    private static void ValidatePassword(string password)
    {
        if (string.IsNullOrWhiteSpace(password) || password.Length < 8)
            throw new InvalidOperationException("A senha deve possuir pelo menos 8 caracteres.");
    }

    private static UserResponseDTO MapToDTO(User user) => new(
        user.Id,
        user.Nome,
        user.Email,
        user.DataNascimento,
        user.Role,
        user.CriadoEm,
        user.Sessions?.Count ?? 0,
        user.MoodEntries?.Count ?? 0
    );
}
''')

write('Services/Interfaces/IServices.cs', r'''using CarePlus.MindfulnessAPI.Models.DTOs;

namespace CarePlus.MindfulnessAPI.Services.Interfaces;

public interface IAuthService
{
    Task<AuthResponseDTO> RegisterAsync(RegisterRequestDTO dto);
    Task<AuthResponseDTO> LoginAsync(LoginRequestDTO dto);
}

public interface IUserService
{
    Task<IEnumerable<UserResponseDTO>> GetAllAsync();
    Task<UserResponseDTO?> GetByIdAsync(Guid id);
    Task<UserResponseDTO> CreateAsync(UserCreateDTO dto);
    Task<UserResponseDTO?> UpdateAsync(Guid id, UserUpdateDTO dto);
    Task<bool> DeleteAsync(Guid id);
}

public interface IMeditationSessionService
{
    Task<IEnumerable<SessionResponseDTO>> GetAllAsync();
    Task<IEnumerable<SessionResponseDTO>> GetByUserIdAsync(Guid userId);
    Task<SessionResponseDTO?> GetByIdAsync(Guid id);
    Task<SessionResponseDTO> CreateAsync(SessionCreateDTO dto);
    Task<SessionResponseDTO?> UpdateAsync(Guid id, SessionUpdateDTO dto);
    Task<bool> DeleteAsync(Guid id);
}

public interface IMoodEntryService
{
    Task<IEnumerable<MoodResponseDTO>> GetAllAsync();
    Task<IEnumerable<MoodResponseDTO>> GetByUserIdAsync(Guid userId);
    Task<MoodResponseDTO?> GetByIdAsync(Guid id);
    Task<MoodResponseDTO> CreateAsync(MoodCreateDTO dto);
    Task<MoodResponseDTO?> UpdateAsync(Guid id, MoodUpdateDTO dto);
    Task<bool> DeleteAsync(Guid id);
}

public interface IWellnessContentService
{
    Task<IEnumerable<ContentResponseDTO>> GetAllAsync();
    Task<IEnumerable<ContentResponseDTO>> GetActiveAsync();
    Task<ContentResponseDTO?> GetByIdAsync(Guid id);
    Task<ContentResponseDTO> CreateAsync(ContentCreateDTO dto);
    Task<ContentResponseDTO?> UpdateAsync(Guid id, ContentUpdateDTO dto);
    Task<bool> DeleteAsync(Guid id);
}
''')

write('Controllers/AuthController.cs', r'''using CarePlus.MindfulnessAPI.Models.DTOs;
using CarePlus.MindfulnessAPI.Services.Interfaces;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace CarePlus.MindfulnessAPI.Controllers;

[ApiController]
[Route("api/[controller]")]
[AllowAnonymous]
public class AuthController : ControllerBase
{
    private readonly IAuthService _authService;

    public AuthController(IAuthService authService)
    {
        _authService = authService;
    }

    /// <summary>
    /// Cadastra um novo usuário comum e retorna um token JWT.
    /// </summary>
    [HttpPost("register")]
    public async Task<ActionResult<ApiResponse<AuthResponseDTO>>> Register([FromBody] RegisterRequestDTO dto)
    {
        var response = await _authService.RegisterAsync(dto);
        return Created(string.Empty, new ApiResponse<AuthResponseDTO>(true, "Usuário registrado com sucesso.", response));
    }

    /// <summary>
    /// Autentica usuário por e-mail e senha e retorna um token JWT.
    /// </summary>
    [HttpPost("login")]
    public async Task<ActionResult<ApiResponse<AuthResponseDTO>>> Login([FromBody] LoginRequestDTO dto)
    {
        var response = await _authService.LoginAsync(dto);
        return Ok(new ApiResponse<AuthResponseDTO>(true, "Login realizado com sucesso.", response));
    }
}
''')

write('Program.cs', r'''using System.Reflection;
using System.Text;
using CarePlus.MindfulnessAPI.Data;
using CarePlus.MindfulnessAPI.Middleware;
using CarePlus.MindfulnessAPI.Repositories;
using CarePlus.MindfulnessAPI.Repositories.Interfaces;
using CarePlus.MindfulnessAPI.Security;
using CarePlus.MindfulnessAPI.Security.Interfaces;
using CarePlus.MindfulnessAPI.Services;
using CarePlus.MindfulnessAPI.Services.Interfaces;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.EntityFrameworkCore;
using Microsoft.IdentityModel.Tokens;
using Microsoft.OpenApi.Models;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseNpgsql(builder.Configuration.GetConnectionString("DefaultConnection")));

builder.Services.AddScoped<IUserRepository, UserRepository>();
builder.Services.AddScoped<IMeditationSessionRepository, MeditationSessionRepository>();
builder.Services.AddScoped<IMoodEntryRepository, MoodEntryRepository>();
builder.Services.AddScoped<IWellnessContentRepository, WellnessContentRepository>();

builder.Services.AddScoped<IAuthService, AuthService>();
builder.Services.AddScoped<IUserService, UserService>();
builder.Services.AddScoped<IMeditationSessionService, MeditationSessionService>();
builder.Services.AddScoped<IMoodEntryService, MoodEntryService>();
builder.Services.AddScoped<IWellnessContentService, WellnessContentService>();
builder.Services.AddScoped<IPasswordHasherService, BCryptPasswordHasherService>();
builder.Services.AddScoped<IJwtTokenService, JwtTokenService>();

var jwtKey = builder.Configuration["Jwt:Key"] ?? throw new InvalidOperationException("Jwt:Key não configurado.");
var jwtIssuer = builder.Configuration["Jwt:Issuer"] ?? throw new InvalidOperationException("Jwt:Issuer não configurado.");
var jwtAudience = builder.Configuration["Jwt:Audience"] ?? throw new InvalidOperationException("Jwt:Audience não configurado.");

builder.Services.AddAuthentication(options =>
{
    options.DefaultAuthenticateScheme = JwtBearerDefaults.AuthenticationScheme;
    options.DefaultChallengeScheme = JwtBearerDefaults.AuthenticationScheme;
})
.AddJwtBearer(options =>
{
    options.RequireHttpsMetadata = false;
    options.SaveToken = false;
    options.TokenValidationParameters = new TokenValidationParameters
    {
        ValidateIssuer = true,
        ValidateAudience = true,
        ValidateLifetime = true,
        ValidateIssuerSigningKey = true,
        ValidIssuer = jwtIssuer,
        ValidAudience = jwtAudience,
        IssuerSigningKey = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(jwtKey)),
        ClockSkew = TimeSpan.Zero
    };
});

builder.Services.AddAuthorization(options =>
{
    options.AddPolicy("AdminOnly", policy => policy.RequireRole("Admin"));
});

builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen(c =>
{
    c.SwaggerDoc("v1", new OpenApiInfo
    {
        Title = "CarePlus Mindfulness API",
        Version = "v1",
        Description = "API de Saúde Mental & Mindfulness - Challenge Care Plus FIAP 2025 - Sprint 4 com autenticação JWT, autorização por perfil e testes."
    });

    c.AddSecurityDefinition("Bearer", new OpenApiSecurityScheme
    {
        Name = "Authorization",
        Type = SecuritySchemeType.Http,
        Scheme = "bearer",
        BearerFormat = "JWT",
        In = ParameterLocation.Header,
        Description = "Informe o token JWT no formato: Bearer {seu_token}"
    });

    c.AddSecurityRequirement(new OpenApiSecurityRequirement
    {
        {
            new OpenApiSecurityScheme
            {
                Reference = new OpenApiReference
                {
                    Type = ReferenceType.SecurityScheme,
                    Id = "Bearer"
                }
            },
            Array.Empty<string>()
        }
    });

    var xmlFile = $"{Assembly.GetExecutingAssembly().GetName().Name}.xml";
    var xmlPath = Path.Combine(AppContext.BaseDirectory, xmlFile);
    if (File.Exists(xmlPath))
        c.IncludeXmlComments(xmlPath);
});

var app = builder.Build();

if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseMiddleware<GlobalExceptionMiddleware>();
app.UseHttpsRedirection();
app.UseAuthentication();
app.UseAuthorization();
app.MapControllers();
app.Run();

public partial class Program { }
''')

print('Autenticação JWT/BCrypt aplicada.')
