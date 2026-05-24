using System.ComponentModel.DataAnnotations;
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
