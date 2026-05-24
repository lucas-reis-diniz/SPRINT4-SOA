using CarePlus.MindfulnessAPI.Mapping.Interfaces;
using CarePlus.MindfulnessAPI.Models.DTOs;
using CarePlus.MindfulnessAPI.Models.Entities;

namespace CarePlus.MindfulnessAPI.Mapping;

public class UserMapper : IModelMapper<User, UserResponseDTO>
{
    public UserResponseDTO Map(User user) => new(
        user.Id,
        user.Nome,
        user.Email,
        user.DataNascimento,
        user.Role,
        user.CriadoEm,
        user.Sessions?.Count ?? 0,
        user.MoodEntries?.Count ?? 0
    );
}
