using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using CarePlus.MindfulnessAPI.Models.Enums;

namespace CarePlus.MindfulnessAPI.Models.Entities;

[Table("mood_entries")]
public class MoodEntry
{
    [Key]
    [Column("id")]
    public Guid Id { get; set; } = Guid.NewGuid();

    [Required]
    [Column("user_id")]
    public Guid UserId { get; set; }

    [Required]
    [Column("nivel_humor")]
    public MoodLevel NivelHumor { get; set; }

    [MaxLength(500)]
    [Column("notas")]
    public string? Notas { get; set; }

    [Column("data_registro")]
    public DateTime DataRegistro { get; set; } = DateTime.UtcNow;

    // Navegação
    [ForeignKey("UserId")]
    public User? User { get; set; }
}
