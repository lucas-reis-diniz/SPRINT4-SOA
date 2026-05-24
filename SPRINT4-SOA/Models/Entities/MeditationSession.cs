using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using CarePlus.MindfulnessAPI.Models.Enums;

namespace CarePlus.MindfulnessAPI.Models.Entities;

[Table("meditation_sessions")]
public class MeditationSession
{
    [Key]
    [Column("id")]
    public Guid Id { get; set; } = Guid.NewGuid();

    [Required]
    [Column("user_id")]
    public Guid UserId { get; set; }

    [Required]
    [Column("tipo")]
    public SessionType Tipo { get; set; }

    [Required]
    [MaxLength(200)]
    [Column("titulo")]
    public string Titulo { get; set; } = string.Empty;

    [Column("duracao_minutos")]
    public int DuracaoMinutos { get; set; }

    [Column("concluida")]
    public bool Concluida { get; set; } = false;

    [MaxLength(500)]
    [Column("observacoes")]
    public string? Observacoes { get; set; }

    [Column("realizada_em")]
    public DateTime RealizadaEm { get; set; } = DateTime.UtcNow;

    [Column("criado_em")]
    public DateTime CriadoEm { get; set; } = DateTime.UtcNow;

    // Navegação
    [ForeignKey("UserId")]
    public User? User { get; set; }
}
