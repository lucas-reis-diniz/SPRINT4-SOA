using CarePlus.MindfulnessAPI.Security.Interfaces;

namespace CarePlus.MindfulnessAPI.Security;

public class DefaultPasswordPolicy : IPasswordPolicy
{
    public void Validate(string password)
    {
        if (string.IsNullOrWhiteSpace(password) || password.Length < 8)
            throw new InvalidOperationException("A senha deve possuir pelo menos 8 caracteres.");

        if (!password.Any(char.IsLetter) || !password.Any(char.IsDigit))
            throw new InvalidOperationException("A senha deve conter letras e números.");
    }
}
