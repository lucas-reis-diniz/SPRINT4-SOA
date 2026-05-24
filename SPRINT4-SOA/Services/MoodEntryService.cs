using CarePlus.MindfulnessAPI.Mapping.Interfaces;
using CarePlus.MindfulnessAPI.Models.DTOs;
using CarePlus.MindfulnessAPI.Models.Entities;
using CarePlus.MindfulnessAPI.Repositories.Interfaces;
using CarePlus.MindfulnessAPI.Services.Interfaces;

namespace CarePlus.MindfulnessAPI.Services;

public class MoodEntryService : IMoodEntryService
{
    private readonly IMoodEntryRepository _repository;
    private readonly IUserRepository _userRepository;
    private readonly IModelMapper<MoodEntry, MoodResponseDTO> _mapper;

    public MoodEntryService(
        IMoodEntryRepository repository,
        IUserRepository userRepository,
        IModelMapper<MoodEntry, MoodResponseDTO> mapper)
    {
        _repository = repository;
        _userRepository = userRepository;
        _mapper = mapper;
    }

    public async Task<IEnumerable<MoodResponseDTO>> GetAllAsync()
    {
        var entries = await _repository.GetAllAsync();
        return entries.Select(_mapper.Map);
    }

    public async Task<IEnumerable<MoodResponseDTO>> GetByUserIdAsync(Guid userId)
    {
        var entries = await _repository.GetByUserIdAsync(userId);
        return entries.Select(_mapper.Map);
    }

    public async Task<MoodResponseDTO?> GetByIdAsync(Guid id)
    {
        var entry = await _repository.GetByIdAsync(id);
        return entry == null ? null : _mapper.Map(entry);
    }

    public async Task<MoodResponseDTO> CreateAsync(MoodCreateDTO dto)
    {
        await EnsureUserExistsAsync(dto.UserId);

        var entry = new MoodEntry
        {
            UserId = dto.UserId,
            NivelHumor = dto.NivelHumor,
            Notas = dto.Notas
        };

        var created = await _repository.CreateAsync(entry);
        var loaded = await _repository.GetByIdAsync(created.Id);
        return _mapper.Map(loaded!);
    }

    public async Task<MoodResponseDTO?> UpdateAsync(Guid id, MoodUpdateDTO dto)
    {
        var entry = await _repository.GetByIdAsync(id);
        if (entry == null) return null;

        entry.NivelHumor = dto.NivelHumor;
        entry.Notas = dto.Notas;

        var updated = await _repository.UpdateAsync(entry);
        return _mapper.Map(updated);
    }

    public async Task<bool> DeleteAsync(Guid id)
    {
        return await _repository.DeleteAsync(id);
    }

    private async Task EnsureUserExistsAsync(Guid userId)
    {
        var userExists = await _userRepository.ExistsAsync(userId);
        if (!userExists)
            throw new InvalidOperationException($"Usuário com ID '{userId}' não encontrado.");
    }
}
