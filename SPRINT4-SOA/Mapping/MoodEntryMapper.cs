using CarePlus.MindfulnessAPI.Mapping.Interfaces;
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
