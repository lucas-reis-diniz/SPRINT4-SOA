using CarePlus.MindfulnessAPI.Mapping.Interfaces;
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
