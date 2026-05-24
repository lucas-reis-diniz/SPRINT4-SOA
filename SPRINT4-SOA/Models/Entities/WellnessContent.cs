using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using CarePlus.MindfulnessAPI.Models.Enums;

namespace CarePlus.MindfulnessAPI.Models.Entities;

[Table("wellness_contents")]
public class WellnessContent
{
    [Key]
    [Column("id")]
    public Guid Id { get; set; } = Guid.NewGuid();

    [Required]
    [MaxLength(200)]
    [Column("titulo")]
    public string Titulo { get; set; } = string.Empty;

    [Required]
    [MaxLength(2000)]
    [Column("descricao")]
    public string Descricao { get; set; } = string.Empty;

    [Required]
    [Column("categoria")]
    public ContentCategory Categoria { get; set; }

    [MaxLength(500)]
    [Column("url_recurso")]
    public string? UrlRecurso { get; set; }

    [Column("duracao_estimada_min")]
    public int? DuracaoEstimadaMin { get; set; }

    [Column("ativo")]
    public bool Ativo { get; set; } = true;

    [Column("criado_em")]
    public DateTime CriadoEm { get; set; } = DateTime.UtcNow;

    [Column("atualizado_em")]
    public DateTime AtualizadoEm { get; set; } = DateTime.UtcNow;
}
