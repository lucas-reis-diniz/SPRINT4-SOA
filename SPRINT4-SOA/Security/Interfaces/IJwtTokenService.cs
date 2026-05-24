using CarePlus.MindfulnessAPI.Models.Entities;

namespace CarePlus.MindfulnessAPI.Security.Interfaces;

public interface IJwtTokenService
{
    (string Token, DateTime ExpiresAt) GenerateToken(User user);
}
