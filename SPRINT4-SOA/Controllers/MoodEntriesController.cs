using CarePlus.MindfulnessAPI.Models.DTOs;
using CarePlus.MindfulnessAPI.Services.Interfaces;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace CarePlus.MindfulnessAPI.Controllers;

[ApiController]
[Route("api/[controller]")]
[Authorize]
public class MoodEntriesController : ControllerBase
{
    private readonly IMoodEntryService _service;

    public MoodEntriesController(IMoodEntryService service)
    {
        _service = service;
    }

    /// <summary>
    /// Lista registros de humor. Requer token JWT válido.
    /// </summary>
    [HttpGet]
    public async Task<ActionResult<ApiResponse<IEnumerable<MoodResponseDTO>>>> GetAll()
    {
        var entries = await _service.GetAllAsync();
        return Ok(new ApiResponse<IEnumerable<MoodResponseDTO>>(true, "Registros de humor listados com sucesso.", entries));
    }

    /// <summary>
    /// Lista registros de humor por usuário. Requer token JWT válido.
    /// </summary>
    [HttpGet("user/{userId:guid}")]
    public async Task<ActionResult<ApiResponse<IEnumerable<MoodResponseDTO>>>> GetByUserId(Guid userId)
    {
        var entries = await _service.GetByUserIdAsync(userId);
        return Ok(new ApiResponse<IEnumerable<MoodResponseDTO>>(true, "Registros de humor do usuário listados com sucesso.", entries));
    }

    /// <summary>
    /// Busca um registro de humor por ID. Requer token JWT válido.
    /// </summary>
    [HttpGet("{id:guid}")]
    public async Task<ActionResult<ApiResponse<MoodResponseDTO>>> GetById(Guid id)
    {
        var entry = await _service.GetByIdAsync(id);
        if (entry == null)
            return NotFound(new ApiErrorResponse(false, $"Registro de humor com ID '{id}' não encontrado.", null));

        return Ok(new ApiResponse<MoodResponseDTO>(true, "Registro de humor encontrado.", entry));
    }

    /// <summary>
    /// Cria um registro de humor. Requer token JWT válido.
    /// </summary>
    [HttpPost]
    public async Task<ActionResult<ApiResponse<MoodResponseDTO>>> Create([FromBody] MoodCreateDTO dto)
    {
        var entry = await _service.CreateAsync(dto);
        return CreatedAtAction(nameof(GetById), new { id = entry.Id },
            new ApiResponse<MoodResponseDTO>(true, "Registro de humor criado com sucesso.", entry));
    }

    /// <summary>
    /// Atualiza um registro de humor. Requer token JWT válido.
    /// </summary>
    [HttpPut("{id:guid}")]
    public async Task<ActionResult<ApiResponse<MoodResponseDTO>>> Update(Guid id, [FromBody] MoodUpdateDTO dto)
    {
        var entry = await _service.UpdateAsync(id, dto);
        if (entry == null)
            return NotFound(new ApiErrorResponse(false, $"Registro de humor com ID '{id}' não encontrado.", null));

        return Ok(new ApiResponse<MoodResponseDTO>(true, "Registro de humor atualizado com sucesso.", entry));
    }

    /// <summary>
    /// Remove um registro de humor. Requer token JWT válido.
    /// </summary>
    [HttpDelete("{id:guid}")]
    public async Task<ActionResult<ApiErrorResponse>> Delete(Guid id)
    {
        var deleted = await _service.DeleteAsync(id);
        if (!deleted)
            return NotFound(new ApiErrorResponse(false, $"Registro de humor com ID '{id}' não encontrado.", null));

        return Ok(new ApiErrorResponse(true, "Registro de humor removido com sucesso.", null));
    }
}
