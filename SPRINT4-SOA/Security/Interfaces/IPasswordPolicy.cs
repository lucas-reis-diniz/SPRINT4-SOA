namespace CarePlus.MindfulnessAPI.Security.Interfaces;

public interface IPasswordPolicy
{
    void Validate(string password);
}
