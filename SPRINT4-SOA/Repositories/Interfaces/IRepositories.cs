using CarePlus.MindfulnessAPI.Models.Entities;

namespace CarePlus.MindfulnessAPI.Repositories.Interfaces;

public interface IUserRepository
{
    Task<IEnumerable<User>> GetAllAsync();
    Task<User?> GetByIdAsync(Guid id);
    Task<User?> GetByEmailAsync(string email);
    Task<User> CreateAsync(User user);
    Task<User> UpdateAsync(User user);
    Task<bool> DeleteAsync(Guid id);
    Task<bool> ExistsAsync(Guid id);
}

public interface IMeditationSessionRepository
{
    Task<IEnumerable<MeditationSession>> GetAllAsync();
    Task<IEnumerable<MeditationSession>> GetByUserIdAsync(Guid userId);
    Task<MeditationSession?> GetByIdAsync(Guid id);
    Task<MeditationSession> CreateAsync(MeditationSession session);
    Task<MeditationSession> UpdateAsync(MeditationSession session);
    Task<bool> DeleteAsync(Guid id);
}

public interface IMoodEntryRepository
{
    Task<IEnumerable<MoodEntry>> GetAllAsync();
    Task<IEnumerable<MoodEntry>> GetByUserIdAsync(Guid userId);
    Task<MoodEntry?> GetByIdAsync(Guid id);
    Task<MoodEntry> CreateAsync(MoodEntry entry);
    Task<MoodEntry> UpdateAsync(MoodEntry entry);
    Task<bool> DeleteAsync(Guid id);
}

public interface IWellnessContentRepository
{
    Task<IEnumerable<WellnessContent>> GetAllAsync();
    Task<IEnumerable<WellnessContent>> GetActiveAsync();
    Task<WellnessContent?> GetByIdAsync(Guid id);
    Task<WellnessContent> CreateAsync(WellnessContent content);
    Task<WellnessContent> UpdateAsync(WellnessContent content);
    Task<bool> DeleteAsync(Guid id);
}
