using CarePlus.MindfulnessAPI.Mapping.Interfaces;
using CarePlus.MindfulnessAPI.Models.DTOs;
using CarePlus.MindfulnessAPI.Models.Entities;
using CarePlus.MindfulnessAPI.Repositories.Interfaces;
using CarePlus.MindfulnessAPI.Services.Interfaces;

namespace CarePlus.MindfulnessAPI.Services;

public class MeditationSessionService : IMeditationSessionService
{
    private readonly IMeditationSessionRepository _repository;
    private readonly IUserRepository _userRepository;
    private readonly IModelMapper<MeditationSession, SessionResponseDTO> _mapper;

    public MeditationSessionService(
        IMeditationSessionRepository repository,
        IUserRepository userRepository,
        IModelMapper<MeditationSession, SessionResponseDTO> mapper)
    {
        _repository = repository;
        _userRepository = userRepository;
        _mapper = mapper;
    }

    public async Task<IEnumerable<SessionResponseDTO>> GetAllAsync()
    {
        var sessions = await _repository.GetAllAsync();
        return sessions.Select(_mapper.Map);
    }

    public async Task<IEnumerable<SessionResponseDTO>> GetByUserIdAsync(Guid userId)
    {
        var sessions = await _repository.GetByUserIdAsync(userId);
        return sessions.Select(_mapper.Map);
    }

    public async Task<SessionResponseDTO?> GetByIdAsync(Guid id)
    {
        var session = await _repository.GetByIdAsync(id);
        return session == null ? null : _mapper.Map(session);
    }

    public async Task<SessionResponseDTO> CreateAsync(SessionCreateDTO dto)
    {
        await EnsureUserExistsAsync(dto.UserId);
        ValidateDuration(dto.DuracaoMinutos);

        var session = new MeditationSession
        {
            UserId = dto.UserId,
            Tipo = dto.Tipo,
            Titulo = dto.Titulo.Trim(),
            DuracaoMinutos = dto.DuracaoMinutos,
            Observacoes = dto.Observacoes
        };

        var created = await _repository.CreateAsync(session);
        var loaded = await _repository.GetByIdAsync(created.Id);
        return _mapper.Map(loaded!);
    }

    public async Task<SessionResponseDTO?> UpdateAsync(Guid id, SessionUpdateDTO dto)
    {
        ValidateDuration(dto.DuracaoMinutos);

        var session = await _repository.GetByIdAsync(id);
        if (session == null) return null;

        session.Tipo = dto.Tipo;
        session.Titulo = dto.Titulo.Trim();
        session.DuracaoMinutos = dto.DuracaoMinutos;
        session.Concluida = dto.Concluida;
        session.Observacoes = dto.Observacoes;

        var updated = await _repository.UpdateAsync(session);
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

    private static void ValidateDuration(int durationMinutes)
    {
        if (durationMinutes <= 0)
            throw new InvalidOperationException("A duração deve ser maior que zero.");
    }
}
