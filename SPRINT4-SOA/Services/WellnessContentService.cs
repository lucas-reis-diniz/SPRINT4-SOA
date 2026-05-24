using CarePlus.MindfulnessAPI.Mapping.Interfaces;
using CarePlus.MindfulnessAPI.Models.DTOs;
using CarePlus.MindfulnessAPI.Models.Entities;
using CarePlus.MindfulnessAPI.Repositories.Interfaces;
using CarePlus.MindfulnessAPI.Services.Interfaces;

namespace CarePlus.MindfulnessAPI.Services;

public class WellnessContentService : IWellnessContentService
{
    private readonly IWellnessContentRepository _repository;
    private readonly IModelMapper<WellnessContent, ContentResponseDTO> _mapper;

    public WellnessContentService(
        IWellnessContentRepository repository,
        IModelMapper<WellnessContent, ContentResponseDTO> mapper)
    {
        _repository = repository;
        _mapper = mapper;
    }

    public async Task<IEnumerable<ContentResponseDTO>> GetAllAsync()
    {
        var contents = await _repository.GetAllAsync();
        return contents.Select(_mapper.Map);
    }

    public async Task<IEnumerable<ContentResponseDTO>> GetActiveAsync()
    {
        var contents = await _repository.GetActiveAsync();
        return contents.Select(_mapper.Map);
    }

    public async Task<ContentResponseDTO?> GetByIdAsync(Guid id)
    {
        var content = await _repository.GetByIdAsync(id);
        return content == null ? null : _mapper.Map(content);
    }

    public async Task<ContentResponseDTO> CreateAsync(ContentCreateDTO dto)
    {
        ValidateDuration(dto.DuracaoEstimadaMin);

        var content = new WellnessContent
        {
            Titulo = dto.Titulo.Trim(),
            Descricao = dto.Descricao.Trim(),
            Categoria = dto.Categoria,
            UrlRecurso = dto.UrlRecurso,
            DuracaoEstimadaMin = dto.DuracaoEstimadaMin
        };

        var created = await _repository.CreateAsync(content);
        return _mapper.Map(created);
    }

    public async Task<ContentResponseDTO?> UpdateAsync(Guid id, ContentUpdateDTO dto)
    {
        ValidateDuration(dto.DuracaoEstimadaMin);

        var content = await _repository.GetByIdAsync(id);
        if (content == null) return null;

        content.Titulo = dto.Titulo.Trim();
        content.Descricao = dto.Descricao.Trim();
        content.Categoria = dto.Categoria;
        content.UrlRecurso = dto.UrlRecurso;
        content.DuracaoEstimadaMin = dto.DuracaoEstimadaMin;
        content.Ativo = dto.Ativo;

        var updated = await _repository.UpdateAsync(content);
        return _mapper.Map(updated);
    }

    public async Task<bool> DeleteAsync(Guid id)
    {
        return await _repository.DeleteAsync(id);
    }

    private static void ValidateDuration(int? durationMinutes)
    {
        if (durationMinutes is <= 0)
            throw new InvalidOperationException("A duração estimada deve ser maior que zero quando informada.");
    }
}
