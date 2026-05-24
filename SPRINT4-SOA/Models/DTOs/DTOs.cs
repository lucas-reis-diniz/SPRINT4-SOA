using CarePlus.MindfulnessAPI.Models.Enums;

namespace CarePlus.MindfulnessAPI.Models.DTOs;

// ===== AUTH DTOs =====
public record RegisterRequestDTO(
    string Nome,
    string Email,
    string Senha,
    DateOnly? DataNascimento
);

public record LoginRequestDTO(
    string Email,
    string Senha
);

public record AuthResponseDTO(
    string Token,
    DateTime ExpiraEm,
    UserResponseDTO Usuario
);

// ===== USER DTOs =====
public record UserCreateDTO(
    string Nome,
    string Email,
    string Senha,
    DateOnly? DataNascimento,
    UserRole Role = UserRole.User
);

public record UserUpdateDTO(
    string Nome,
    string Email,
    DateOnly? DataNascimento,
    UserRole Role
);

public record UserResponseDTO(
    Guid Id,
    string Nome,
    string Email,
    DateOnly? DataNascimento,
    UserRole Role,
    DateTime CriadoEm,
    int TotalSessions,
    int TotalMoodEntries
);

// ===== MEDITATION SESSION DTOs =====
public record SessionCreateDTO(
    Guid UserId,
    SessionType Tipo,
    string Titulo,
    int DuracaoMinutos,
    string? Observacoes
);

public record SessionUpdateDTO(
    SessionType Tipo,
    string Titulo,
    int DuracaoMinutos,
    bool Concluida,
    string? Observacoes
);

public record SessionResponseDTO(
    Guid Id,
    Guid UserId,
    string NomeUsuario,
    SessionType Tipo,
    string Titulo,
    int DuracaoMinutos,
    bool Concluida,
    string? Observacoes,
    DateTime RealizadaEm
);

// ===== MOOD ENTRY DTOs =====
public record MoodCreateDTO(
    Guid UserId,
    MoodLevel NivelHumor,
    string? Notas
);

public record MoodUpdateDTO(
    MoodLevel NivelHumor,
    string? Notas
);

public record MoodResponseDTO(
    Guid Id,
    Guid UserId,
    string NomeUsuario,
    MoodLevel NivelHumor,
    string NivelHumorDescricao,
    string? Notas,
    DateTime DataRegistro
);

// ===== WELLNESS CONTENT DTOs =====
public record ContentCreateDTO(
    string Titulo,
    string Descricao,
    ContentCategory Categoria,
    string? UrlRecurso,
    int? DuracaoEstimadaMin
);

public record ContentUpdateDTO(
    string Titulo,
    string Descricao,
    ContentCategory Categoria,
    string? UrlRecurso,
    int? DuracaoEstimadaMin,
    bool Ativo
);

public record ContentResponseDTO(
    Guid Id,
    string Titulo,
    string Descricao,
    ContentCategory Categoria,
    string? UrlRecurso,
    int? DuracaoEstimadaMin,
    bool Ativo,
    DateTime CriadoEm
);

// ===== API RESPONSE WRAPPER =====
public record ApiResponse<T>(
    bool Sucesso,
    string Mensagem,
    T? Dados
);

public record ApiErrorResponse(
    bool Sucesso,
    string Mensagem,
    List<string>? Erros
);
