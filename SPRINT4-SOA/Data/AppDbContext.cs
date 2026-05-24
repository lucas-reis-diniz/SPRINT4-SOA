using CarePlus.MindfulnessAPI.Models.Entities;
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
                PasswordHash = "$2b$11$FbIkP7XIZUKs/00gs6Z0yOswD4wiCZSjIIOktQh6VVx4VE5a9j/vu",
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
                PasswordHash = "$2b$11$FbIkP7XIZUKs/00gs6Z0yOswD4wiCZSjIIOktQh6VVx4VE5a9j/vu",
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
