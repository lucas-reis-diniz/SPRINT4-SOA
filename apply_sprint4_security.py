from pathlib import Path

root = Path('/home/ubuntu/SPRINT3-SOA')

files = {
'CarePlus.MindfulnessAPI.csproj': r'''<Project Sdk="Microsoft.NET.Sdk.Web">

  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
    <GenerateDocumentationFile>true</GenerateDocumentationFile>
    <NoWarn>$(NoWarn);1591</NoWarn>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="BCrypt.Net-Next" Version="4.0.3" />
    <PackageReference Include="Microsoft.AspNetCore.Authentication.JwtBearer" Version="8.0.8" />
    <PackageReference Include="Microsoft.EntityFrameworkCore" Version="8.0.8" />
    <PackageReference Include="Microsoft.EntityFrameworkCore.Design" Version="8.0.8">
      <PrivateAssets>all</PrivateAssets>
      <IncludeAssets>runtime; build; native; contentfiles; analyzers; buildtransitive</IncludeAssets>
    </PackageReference>
    <PackageReference Include="Npgsql.EntityFrameworkCore.PostgreSQL" Version="8.0.4" />
    <PackageReference Include="Swashbuckle.AspNetCore" Version="6.5.0" />
  </ItemGroup>

</Project>
''',
'appsettings.json': r'''{
  "ConnectionStrings": {
    "DefaultConnection": "Host=localhost;Port=5432;Database=careplus_mindfulness;Username=postgres;Password=postgres"
  },
  "Jwt": {
    "Issuer": "CarePlus.MindfulnessAPI",
    "Audience": "CarePlus.MindfulnessAPI.Client",
    "Key": "CarePlus-Sprint4-Development-Key-Change-In-Production-2026",
    "ExpirationMinutes": 120
  },
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft.AspNetCore": "Warning"
    }
  },
  "AllowedHosts": "*"
}
''',
'Models/Enums/Enums.cs': r'''namespace CarePlus.MindfulnessAPI.Models.Enums;

public enum MoodLevel
{
    MuitoBaixo = 1,
    Baixo = 2,
    Neutro = 3,
    Bom = 4,
    Excelente = 5
}

public enum SessionType
{
    Meditacao,
    Respiracao,
    BodyScan,
    Visualizacao,
    Relaxamento
}

public enum ContentCategory
{
    Artigo,
    Audio,
    Video,
    Exercicio,
    Dica
}

public enum UserRole
{
    User,
    Admin
}
''',
'Models/Entities/User.cs': r'''using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using CarePlus.MindfulnessAPI.Models.Enums;

namespace CarePlus.MindfulnessAPI.Models.Entities;

[Table("users")]
public class User
{
    [Key]
    [Column("id")]
    public Guid Id { get; set; } = Guid.NewGuid();

    [Required]
    [MaxLength(150)]
    [Column("nome")]
    public string Nome { get; set; } = string.Empty;

    [Required]
    [MaxLength(200)]
    [EmailAddress]
    [Column("email")]
    public string Email { get; set; } = string.Empty;

    [Required]
    [MaxLength(255)]
    [Column("password_hash")]
    public string PasswordHash { get; set; } = string.Empty;

    [Required]
    [Column("role")]
    public UserRole Role { get; set; } = UserRole.User;

    [Column("data_nascimento")]
    public DateOnly? DataNascimento { get; set; }

    [Column("criado_em")]
    public DateTime CriadoEm { get; set; } = DateTime.UtcNow;

    [Column("atualizado_em")]
    public DateTime AtualizadoEm { get; set; } = DateTime.UtcNow;

    public ICollection<MeditationSession> Sessions { get; set; } = new List<MeditationSession>();
    public ICollection<MoodEntry> MoodEntries { get; set; } = new List<MoodEntry>();
}
''',
'Models/DTOs/DTOs.cs': r'''using CarePlus.MindfulnessAPI.Models.Enums;

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
''',
'Data/AppDbContext.cs': r'''using CarePlus.MindfulnessAPI.Models.Entities;
using CarePlus.MindfulnessAPI.Models.Enums;
using Microsoft.EntityFrameworkCore;

namespace CarePlus.MindfulnessAPI.Data;

public class AppDbContext : DbContext
{
    public AppDbContext(DbContextOptions<AppDbContext> options) : base(options) { }

    public DbSet<User> Users { get; set; }
    public DbSet<MeditationSession> MeditationSessions { get; set; }
    public DbSet<MoodEntry> MoodEntries { get; set; }
    public DbSet<WellnessContent> WellnessContents { get; set; }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder);

        modelBuilder.Entity<User>(entity =>
        {
            entity.HasIndex(u => u.Email).IsUnique();
            entity.Property(u => u.Role).HasConversion<string>();
            entity.HasMany(u => u.Sessions)
                  .WithOne(s => s.User)
                  .HasForeignKey(s => s.UserId)
                  .OnDelete(DeleteBehavior.Cascade);
            entity.HasMany(u => u.MoodEntries)
                  .WithOne(m => m.User)
                  .HasForeignKey(m => m.UserId)
                  .OnDelete(DeleteBehavior.Cascade);
        });

        modelBuilder.Entity<MeditationSession>(entity =>
        {
            entity.Property(s => s.Tipo).HasConversion<string>();
        });

        modelBuilder.Entity<MoodEntry>(entity =>
        {
            entity.Property(m => m.NivelHumor).HasConversion<string>();
        });

        modelBuilder.Entity<WellnessContent>(entity =>
        {
            entity.Property(c => c.Categoria).HasConversion<string>();
        });

        SeedData(modelBuilder);
    }

    private static void SeedData(ModelBuilder modelBuilder)
    {
        var userId1 = Guid.Parse("a1b2c3d4-e5f6-7890-abcd-ef1234567890");
        var userId2 = Guid.Parse("b2c3d4e5-f6a7-8901-bcde-f12345678901");

        modelBuilder.Entity<User>().HasData(
            new User
            {
                Id = userId1,
                Nome = "Maria Silva",
                Email = "maria.silva@careplus.com",
                PasswordHash = "$2a$11$H5NZa1PQUCByewMgbzxDxOih5WxUxMtZKsk/1K4uFTIB5B2dG78Hu",
                Role = UserRole.Admin,
                DataNascimento = new DateOnly(1990, 5, 15),
                CriadoEm = new DateTime(2025, 1, 1, 0, 0, 0, DateTimeKind.Utc),
                AtualizadoEm = new DateTime(2025, 1, 1, 0, 0, 0, DateTimeKind.Utc)
            },
            new User
            {
                Id = userId2,
                Nome = "João Santos",
                Email = "joao.santos@careplus.com",
                PasswordHash = "$2a$11$H5NZa1PQUCByewMgbzxDxOih5WxUxMtZKsk/1K4uFTIB5B2dG78Hu",
                Role = UserRole.User,
                DataNascimento = new DateOnly(1985, 8, 22),
                CriadoEm = new DateTime(2025, 1, 1, 0, 0, 0, DateTimeKind.Utc),
                AtualizadoEm = new DateTime(2025, 1, 1, 0, 0, 0, DateTimeKind.Utc)
            }
        );

        modelBuilder.Entity<WellnessContent>().HasData(
            new WellnessContent
            {
                Id = Guid.Parse("c3d4e5f6-a7b8-9012-cdef-123456789012"),
                Titulo = "Introdução à Meditação Mindfulness",
                Descricao = "Aprenda os fundamentos da meditação mindfulness e como ela pode melhorar sua saúde mental e bem-estar diário.",
                Categoria = ContentCategory.Artigo,
                DuracaoEstimadaMin = 10,
                Ativo = true,
                CriadoEm = new DateTime(2025, 1, 1, 0, 0, 0, DateTimeKind.Utc),
                AtualizadoEm = new DateTime(2025, 1, 1, 0, 0, 0, DateTimeKind.Utc)
            },
            new WellnessContent
            {
                Id = Guid.Parse("d4e5f6a7-b8c9-0123-defa-234567890123"),
                Titulo = "Respiração 4-7-8 para Ansiedade",
                Descricao = "Técnica de respiração comprovada para reduzir ansiedade: inspire por 4 segundos, segure por 7, expire por 8.",
                Categoria = ContentCategory.Exercicio,
                DuracaoEstimadaMin = 5,
                Ativo = true,
                CriadoEm = new DateTime(2025, 1, 1, 0, 0, 0, DateTimeKind.Utc),
                AtualizadoEm = new DateTime(2025, 1, 1, 0, 0, 0, DateTimeKind.Utc)
            },
            new WellnessContent
            {
                Id = Guid.Parse("e5f6a7b8-c9d0-1234-efab-345678901234"),
                Titulo = "5 Dicas para Melhorar o Sono",
                Descricao = "Rotinas e hábitos simples que podem transformar a qualidade do seu sono e impactar positivamente sua saúde mental.",
                Categoria = ContentCategory.Dica,
                DuracaoEstimadaMin = 7,
                Ativo = true,
                CriadoEm = new DateTime(2025, 1, 1, 0, 0, 0, DateTimeKind.Utc),
                AtualizadoEm = new DateTime(2025, 1, 1, 0, 0, 0, DateTimeKind.Utc)
            }
        );
    }
}
'''
}

for relative_path, content in files.items():
    path = root / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')

print(f"Arquivos base atualizados: {len(files)}")
