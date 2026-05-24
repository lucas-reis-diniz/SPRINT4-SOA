using CarePlus.MindfulnessAPI.Models.DTOs;
using CarePlus.MindfulnessAPI.Services.Interfaces;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace CarePlus.MindfulnessAPI.Controllers;

[ApiController]
[Route("api/[controller]")]
[Authorize]
public class MeditationSessionsController : ControllerBase
{
    private readonly IMeditationSessionService _service;

    public MeditationSessionsController(IMeditationSessionService service)
    {
        _service = service;
    }

    /// <summary>
    /// Lista todas as sessões de meditação. Requer token JWT válido.
    /// </summary>
    [HttpGet]
    public async Task<ActionResult<ApiResponse<IEnumerable<SessionResponseDTO>>>> GetAll()
    {
        var sessions = await _service.GetAllAsync();
        return Ok(new ApiResponse<IEnumerable<SessionResponseDTO>>(true, "Sessões listadas com sucesso.", sessions));
    }

    /// <summary>
    /// Lista sessões de meditação por usuário. Requer token JWT válido.
    /// </summary>
    [HttpGet("user/{userId:guid}")]
    public async Task<ActionResult<ApiResponse<IEnumerable<SessionResponseDTO>>>> GetByUserId(Guid userId)
    {
        var sessions = await _service.GetByUserIdAsync(userId);
        return Ok(new ApiResponse<IEnumerable<SessionResponseDTO>>(true, "Sessões do usuário listadas com sucesso.", sessions));
    }

    /// <summary>
    /// Busca uma sessão de meditação pelo ID. Requer token JWT válido.
    /// </summary>
    [HttpGet("{id:guid}")]
    public async Task<ActionResult<ApiResponse<SessionResponseDTO>>> GetById(Guid id)
    {
        var session = await _service.GetByIdAsync(id);
        if (session == null)
            return NotFound(new ApiErrorResponse(false, $"Sessão com ID '{id}' não encontrada.", null));

        return Ok(new ApiResponse<SessionResponseDTO>(true, "Sessão encontrada.", session));
    }

    /// <summary>
    /// Cria uma sessão de meditação. Requer token JWT válido.
    /// </summary>
    [HttpPost]
    public async Task<ActionResult<ApiResponse<SessionResponseDTO>>> Create([FromBody] SessionCreateDTO dto)
    {
        var session = await _service.CreateAsync(dto);
        return CreatedAtAction(nameof(GetById), new { id = session.Id },
            new ApiResponse<SessionResponseDTO>(true, "Sessão criada com sucesso.", session));
    }

    /// <summary>
    /// Atualiza uma sessão de meditação. Requer token JWT válido.
    /// </summary>
    [HttpPut("{id:guid}")]
    public async Task<ActionResult<ApiResponse<SessionResponseDTO>>> Update(Guid id, [FromBody] SessionUpdateDTO dto)
    {
        var session = await _service.UpdateAsync(id, dto);
        if (session == null)
            return NotFound(new ApiErrorResponse(false, $"Sessão com ID '{id}' não encontrada.", null));

        return Ok(new ApiResponse<SessionResponseDTO>(true, "Sessão atualizada com sucesso.", session));
    }

    /// <summary>
    /// Remove uma sessão de meditação. Requer token JWT válido.
    /// </summary>
    [HttpDelete("{id:guid}")]
    public async Task<ActionResult<ApiErrorResponse>> Delete(Guid id)
    {
        var deleted = await _service.DeleteAsync(id);
        if (!deleted)
            return NotFound(new ApiErrorResponse(false, $"Sessão com ID '{id}' não encontrada.", null));

        return Ok(new ApiErrorResponse(true, "Sessão removida com sucesso.", null));
    }
}
