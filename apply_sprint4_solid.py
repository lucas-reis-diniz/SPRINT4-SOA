from pathlib import Path
root = Path('/home/ubuntu/SPRINT3-SOA')

def write(relative, content):
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')

write('Mapping/Interfaces/IModelMapper.cs', r'''namespace CarePlus.MindfulnessAPI.Mapping.Interfaces;

public interface IModelMapper<in TSource, out TDestination>
{
    TDestination Map(TSource source);
}
''')

write('Mapping/UserMapper.cs', r'''using CarePlus.MindfulnessAPI.Mapping.Interfaces;
using CarePlus.MindfulnessAPI.Models.DTOs;
using CarePlus.MindfulnessAPI.Models.Entities;

namespace CarePlus.MindfulnessAPI.Mapping;

public class UserMapper : IModelMapper<User, UserResponseDTO>
{
    public UserResponseDTO Map(User user) => new(
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

write('Mapping/MeditationSessionMapper.cs', r'''using CarePlus.MindfulnessAPI.Mapping.Interfaces;
using CarePlus.MindfulnessAPI.Models.DTOs;
using CarePlus.MindfulnessAPI.Models.Entities;

namespace CarePlus.MindfulnessAPI.Mapping;

public class MeditationSessionMapper : IModelMapper<MeditationSession, SessionResponseDTO>
{
    public SessionResponseDTO Map(MeditationSession session) => new(
        session.Id,
        session.UserId,
        session.User?.Nome ?? "Desconhecido",
        session.Tipo,
        session.Titulo,
        session.DuracaoMinutos,
        session.Concluida,
        session.Observacoes,
        session.RealizadaEm
    );
}
''')

write('Mapping/MoodEntryMapper.cs', r'''using CarePlus.MindfulnessAPI.Mapping.Interfaces;
using CarePlus.MindfulnessAPI.Models.DTOs;
using CarePlus.MindfulnessAPI.Models.Entities;

namespace CarePlus.MindfulnessAPI.Mapping;

public class MoodEntryMapper : IModelMapper<MoodEntry, MoodResponseDTO>
{
    public MoodResponseDTO Map(MoodEntry moodEntry) => new(
        moodEntry.Id,
        moodEntry.UserId,
        moodEntry.User?.Nome ?? "Desconhecido",
        moodEntry.NivelHumor,
        moodEntry.NivelHumor.ToString(),
        moodEntry.Notas,
        moodEntry.DataRegistro
    );
}
''')

write('Mapping/WellnessContentMapper.cs', r'''using CarePlus.MindfulnessAPI.Mapping.Interfaces;
using CarePlus.MindfulnessAPI.Models.DTOs;
using CarePlus.MindfulnessAPI.Models.Entities;

namespace CarePlus.MindfulnessAPI.Mapping;

public class WellnessContentMapper : IModelMapper<WellnessContent, ContentResponseDTO>
{
    public ContentResponseDTO Map(WellnessContent content) => new(
        content.Id,
        content.Titulo,
        content.Descricao,
        content.Categoria,
        content.UrlRecurso,
        content.DuracaoEstimadaMin,
        content.Ativo,
        content.CriadoEm
    );
}
''')

write('Security/Interfaces/IPasswordPolicy.cs', r'''namespace CarePlus.MindfulnessAPI.Security.Interfaces;

public interface IPasswordPolicy
{
    void Validate(string password);
}
''')

write('Security/DefaultPasswordPolicy.cs', r'''using CarePlus.MindfulnessAPI.Security.Interfaces;

namespace CarePlus.MindfulnessAPI.Security;

public class DefaultPasswordPolicy : IPasswordPolicy
{
    public void Validate(string password)
    {
        if (string.IsNullOrWhiteSpace(password) || password.Length < 8)
            throw new InvalidOperationException("A senha deve possuir pelo menos 8 caracteres.");

        if (!password.Any(char.IsLetter) || !password.Any(char.IsDigit))
            throw new InvalidOperationException("A senha deve conter letras e números.");
    }
}
''')

write('Services/AuthService.cs', r'''using CarePlus.MindfulnessAPI.Mapping.Interfaces;
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
''')

write('Services/UserService.cs', r'''using CarePlus.MindfulnessAPI.Mapping.Interfaces;
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
''')

write('Services/MeditationSessionService.cs', r'''using CarePlus.MindfulnessAPI.Mapping.Interfaces;
using CarePlus.MindfulnessAPI.Models.DTOs;
using CarePlus.MindfulnessAPI.Models.Entities;
using CarePlus.MindfulnessAPI.Repositories.Interfaces;
using CarePlus.MindfulnessAPI.Services.Interfaces;

namespace CarePlus.MindfulnessAPI.Services;

public class MeditationSessionService : IMeditationSessionService
{
    private readonly IMeditationSessionRepository _repository;
    private readonly IUserRepository _userRepository;
    private readonly IModelMapper<MeditationSession, SessionResponseDTO> _mapper;

    public MeditationSessionService(
        IMeditationSessionRepository repository,
        IUserRepository userRepository,
        IModelMapper<MeditationSession, SessionResponseDTO> mapper)
    {
        _repository = repository;
        _userRepository = userRepository;
        _mapper = mapper;
    }

    public async Task<IEnumerable<SessionResponseDTO>> GetAllAsync()
    {
        var sessions = await _repository.GetAllAsync();
        return sessions.Select(_mapper.Map);
    }

    public async Task<IEnumerable<SessionResponseDTO>> GetByUserIdAsync(Guid userId)
    {
        var sessions = await _repository.GetByUserIdAsync(userId);
        return sessions.Select(_mapper.Map);
    }

    public async Task<SessionResponseDTO?> GetByIdAsync(Guid id)
    {
        var session = await _repository.GetByIdAsync(id);
        return session == null ? null : _mapper.Map(session);
    }

    public async Task<SessionResponseDTO> CreateAsync(SessionCreateDTO dto)
    {
        await EnsureUserExistsAsync(dto.UserId);
        ValidateDuration(dto.DuracaoMinutos);

        var session = new MeditationSession
        {
            UserId = dto.UserId,
            Tipo = dto.Tipo,
            Titulo = dto.Titulo.Trim(),
            DuracaoMinutos = dto.DuracaoMinutos,
            Observacoes = dto.Observacoes
        };

        var created = await _repository.CreateAsync(session);
        var loaded = await _repository.GetByIdAsync(created.Id);
        return _mapper.Map(loaded!);
    }

    public async Task<SessionResponseDTO?> UpdateAsync(Guid id, SessionUpdateDTO dto)
    {
        ValidateDuration(dto.DuracaoMinutos);

        var session = await _repository.GetByIdAsync(id);
        if (session == null) return null;

        session.Tipo = dto.Tipo;
        session.Titulo = dto.Titulo.Trim();
        session.DuracaoMinutos = dto.DuracaoMinutos;
        session.Concluida = dto.Concluida;
        session.Observacoes = dto.Observacoes;

        var updated = await _repository.UpdateAsync(session);
        return _mapper.Map(updated);
    }

    public async Task<bool> DeleteAsync(Guid id)
    {
        return await _repository.DeleteAsync(id);
    }

    private async Task EnsureUserExistsAsync(Guid userId)
    {
        var userExists = await _userRepository.ExistsAsync(userId);
        if (!userExists)
            throw new InvalidOperationException($"Usuário com ID '{userId}' não encontrado.");
    }

    private static void ValidateDuration(int durationMinutes)
    {
        if (durationMinutes <= 0)
            throw new InvalidOperationException("A duração deve ser maior que zero.");
    }
}
''')

write('Services/MoodEntryService.cs', r'''using CarePlus.MindfulnessAPI.Mapping.Interfaces;
using CarePlus.MindfulnessAPI.Models.DTOs;
using CarePlus.MindfulnessAPI.Models.Entities;
using CarePlus.MindfulnessAPI.Repositories.Interfaces;
using CarePlus.MindfulnessAPI.Services.Interfaces;

namespace CarePlus.MindfulnessAPI.Services;

public class MoodEntryService : IMoodEntryService
{
    private readonly IMoodEntryRepository _repository;
    private readonly IUserRepository _userRepository;
    private readonly IModelMapper<MoodEntry, MoodResponseDTO> _mapper;

    public MoodEntryService(
        IMoodEntryRepository repository,
        IUserRepository userRepository,
        IModelMapper<MoodEntry, MoodResponseDTO> mapper)
    {
        _repository = repository;
        _userRepository = userRepository;
        _mapper = mapper;
    }

    public async Task<IEnumerable<MoodResponseDTO>> GetAllAsync()
    {
        var entries = await _repository.GetAllAsync();
        return entries.Select(_mapper.Map);
    }

    public async Task<IEnumerable<MoodResponseDTO>> GetByUserIdAsync(Guid userId)
    {
        var entries = await _repository.GetByUserIdAsync(userId);
        return entries.Select(_mapper.Map);
    }

    public async Task<MoodResponseDTO?> GetByIdAsync(Guid id)
    {
        var entry = await _repository.GetByIdAsync(id);
        return entry == null ? null : _mapper.Map(entry);
    }

    public async Task<MoodResponseDTO> CreateAsync(MoodCreateDTO dto)
    {
        await EnsureUserExistsAsync(dto.UserId);

        var entry = new MoodEntry
        {
            UserId = dto.UserId,
            NivelHumor = dto.NivelHumor,
            Notas = dto.Notas
        };

        var created = await _repository.CreateAsync(entry);
        var loaded = await _repository.GetByIdAsync(created.Id);
        return _mapper.Map(loaded!);
    }

    public async Task<MoodResponseDTO?> UpdateAsync(Guid id, MoodUpdateDTO dto)
    {
        var entry = await _repository.GetByIdAsync(id);
        if (entry == null) return null;

        entry.NivelHumor = dto.NivelHumor;
        entry.Notas = dto.Notas;

        var updated = await _repository.UpdateAsync(entry);
        return _mapper.Map(updated);
    }

    public async Task<bool> DeleteAsync(Guid id)
    {
        return await _repository.DeleteAsync(id);
    }

    private async Task EnsureUserExistsAsync(Guid userId)
    {
        var userExists = await _userRepository.ExistsAsync(userId);
        if (!userExists)
            throw new InvalidOperationException($"Usuário com ID '{userId}' não encontrado.");
    }
}
''')

write('Services/WellnessContentService.cs', r'''using CarePlus.MindfulnessAPI.Mapping.Interfaces;
using CarePlus.MindfulnessAPI.Models.DTOs;
using CarePlus.MindfulnessAPI.Models.Entities;
using CarePlus.MindfulnessAPI.Repositories.Interfaces;
using CarePlus.MindfulnessAPI.Services.Interfaces;

namespace CarePlus.MindfulnessAPI.Services;

public class WellnessContentService : IWellnessContentService
{
    private readonly IWellnessContentRepository _repository;
    private readonly IModelMapper<WellnessContent, ContentResponseDTO> _mapper;

    public WellnessContentService(
        IWellnessContentRepository repository,
        IModelMapper<WellnessContent, ContentResponseDTO> mapper)
    {
        _repository = repository;
        _mapper = mapper;
    }

    public async Task<IEnumerable<ContentResponseDTO>> GetAllAsync()
    {
        var contents = await _repository.GetAllAsync();
        return contents.Select(_mapper.Map);
    }

    public async Task<IEnumerable<ContentResponseDTO>> GetActiveAsync()
    {
        var contents = await _repository.GetActiveAsync();
        return contents.Select(_mapper.Map);
    }

    public async Task<ContentResponseDTO?> GetByIdAsync(Guid id)
    {
        var content = await _repository.GetByIdAsync(id);
        return content == null ? null : _mapper.Map(content);
    }

    public async Task<ContentResponseDTO> CreateAsync(ContentCreateDTO dto)
    {
        ValidateDuration(dto.DuracaoEstimadaMin);

        var content = new WellnessContent
        {
            Titulo = dto.Titulo.Trim(),
            Descricao = dto.Descricao.Trim(),
            Categoria = dto.Categoria,
            UrlRecurso = dto.UrlRecurso,
            DuracaoEstimadaMin = dto.DuracaoEstimadaMin
        };

        var created = await _repository.CreateAsync(content);
        return _mapper.Map(created);
    }

    public async Task<ContentResponseDTO?> UpdateAsync(Guid id, ContentUpdateDTO dto)
    {
        ValidateDuration(dto.DuracaoEstimadaMin);

        var content = await _repository.GetByIdAsync(id);
        if (content == null) return null;

        content.Titulo = dto.Titulo.Trim();
        content.Descricao = dto.Descricao.Trim();
        content.Categoria = dto.Categoria;
        content.UrlRecurso = dto.UrlRecurso;
        content.DuracaoEstimadaMin = dto.DuracaoEstimadaMin;
        content.Ativo = dto.Ativo;

        var updated = await _repository.UpdateAsync(content);
        return _mapper.Map(updated);
    }

    public async Task<bool> DeleteAsync(Guid id)
    {
        return await _repository.DeleteAsync(id);
    }

    private static void ValidateDuration(int? durationMinutes)
    {
        if (durationMinutes is <= 0)
            throw new InvalidOperationException("A duração estimada deve ser maior que zero quando informada.");
    }
}
''')

print('Refatoração SOLID aplicada.')
