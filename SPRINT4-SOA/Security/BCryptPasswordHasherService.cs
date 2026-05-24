using CarePlus.MindfulnessAPI.Security.Interfaces;

namespace CarePlus.MindfulnessAPI.Security;

public class BCryptPasswordHasherService : IPasswordHasherService
{
    private const int WorkFactor = 11;

    public string Hash(string password)
    {
        if (string.IsNullOrWhiteSpace(password))
            throw new InvalidOperationException("A senha é obrigatória.");

        return BCrypt.Net.BCrypt.HashPassword(password, WorkFactor);
    }

    public bool Verify(string password, string passwordHash)
    {
        if (string.IsNullOrWhiteSpace(password) || string.IsNullOrWhiteSpace(passwordHash))
            return false;

        return BCrypt.Net.BCrypt.Verify(password, passwordHash);
    }
}
