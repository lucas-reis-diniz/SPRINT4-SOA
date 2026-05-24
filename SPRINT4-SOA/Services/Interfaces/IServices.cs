using CarePlus.MindfulnessAPI.Models.DTOs;

namespace CarePlus.MindfulnessAPI.Services.Interfaces;

public interface IAuthService
{
    Task<AuthResponseDTO> RegisterAsync(RegisterRequestDTO dto);
    Task<AuthResponseDTO> LoginAsync(LoginRequestDTO dto);
}

public interface IUserService
{
    Task<IEnumerable<UserResponseDTO>> GetAllAsync();
    Task<UserResponseDTO?> GetByIdAsync(Guid id);
    Task<UserResponseDTO> CreateAsync(UserCreateDTO dto);
    Task<UserResponseDTO?> UpdateAsync(Guid id, UserUpdateDTO dto);
    Task<bool> DeleteAsync(Guid id);
}

public interface IMeditationSessionService
{
    Task<IEnumerable<SessionResponseDTO>> GetAllAsync();
    Task<IEnumerable<SessionResponseDTO>> GetByUserIdAsync(Guid userId);
    Task<SessionResponseDTO?> GetByIdAsync(Guid id);
    Task<SessionResponseDTO> CreateAsync(SessionCreateDTO dto);
    Task<SessionResponseDTO?> UpdateAsync(Guid id, SessionUpdateDTO dto);
    Task<bool> DeleteAsync(Guid id);
}

public interface IMoodEntryService
{
    Task<IEnumerable<MoodResponseDTO>> GetAllAsync();
    Task<IEnumerable<MoodResponseDTO>> GetByUserIdAsync(Guid userId);
    Task<MoodResponseDTO?> GetByIdAsync(Guid id);
    Task<MoodResponseDTO> CreateAsync(MoodCreateDTO dto);
    Task<MoodResponseDTO?> UpdateAsync(Guid id, MoodUpdateDTO dto);
    Task<bool> DeleteAsync(Guid id);
}

public interface IWellnessContentService
{
    Task<IEnumerable<ContentResponseDTO>> GetAllAsync();
    Task<IEnumerable<ContentResponseDTO>> GetActiveAsync();
    Task<ContentResponseDTO?> GetByIdAsync(Guid id);
    Task<ContentResponseDTO> CreateAsync(ContentCreateDTO dto);
    Task<ContentResponseDTO?> UpdateAsync(Guid id, ContentUpdateDTO dto);
    Task<bool> DeleteAsync(Guid id);
}
