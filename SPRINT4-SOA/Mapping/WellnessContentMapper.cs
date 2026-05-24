using CarePlus.MindfulnessAPI.Mapping.Interfaces;
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
