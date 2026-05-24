using CarePlus.MindfulnessAPI.Models.DTOs;
using CarePlus.MindfulnessAPI.Models.Enums;
using CarePlus.MindfulnessAPI.Services.Interfaces;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace CarePlus.MindfulnessAPI.Controllers;

[ApiController]
[Route("api/[controller]")]
[Authorize]
public class WellnessContentsController : ControllerBase
{
    private readonly IWellnessContentService _service;

    public WellnessContentsController(IWellnessContentService service)
    {
        _service = service;
    }

    /// <summary>
    /// Lista todos os conteúdos, inclusive inativos. Requer perfil Admin.
    /// </summary>
    [HttpGet]
    [Authorize(Roles = nameof(UserRole.Admin))]
    public async Task<ActionResult<ApiResponse<IEnumerable<ContentResponseDTO>>>> GetAll()
    {
        var contents = await _service.GetAllAsync();
        return Ok(new ApiResponse<IEnumerable<ContentResponseDTO>>(true, "Conteúdos listados com sucesso.", contents));
    }

    /// <summary>
    /// Lista conteúdos ativos. Endpoint público para consulta.
    /// </summary>
    [HttpGet("active")]
    [AllowAnonymous]
    public async Task<ActionResult<ApiResponse<IEnumerable<ContentResponseDTO>>>> GetActive()
    {
        var contents = await _service.GetActiveAsync();
        return Ok(new ApiResponse<IEnumerable<ContentResponseDTO>>(true, "Conteúdos ativos listados com sucesso.", contents));
    }

    /// <summary>
    /// Busca um conteúdo pelo ID. Requer token JWT válido.
    /// </summary>
    [HttpGet("{id:guid}")]
    public async Task<ActionResult<ApiResponse<ContentResponseDTO>>> GetById(Guid id)
    {
        var content = await _service.GetByIdAsync(id);
        if (content == null)
            return NotFound(new ApiErrorResponse(false, $"Conteúdo com ID '{id}' não encontrado.", null));

        return Ok(new ApiResponse<ContentResponseDTO>(true, "Conteúdo encontrado.", content));
    }

    /// <summary>
    /// Cria conteúdo de bem-estar. Requer perfil Admin.
    /// </summary>
    [HttpPost]
    [Authorize(Roles = nameof(UserRole.Admin))]
    public async Task<ActionResult<ApiResponse<ContentResponseDTO>>> Create([FromBody] ContentCreateDTO dto)
    {
        var content = await _service.CreateAsync(dto);
        return CreatedAtAction(nameof(GetById), new { id = content.Id },
            new ApiResponse<ContentResponseDTO>(true, "Conteúdo criado com sucesso.", content));
    }

    /// <summary>
    /// Atualiza conteúdo de bem-estar. Requer perfil Admin.
    /// </summary>
    [HttpPut("{id:guid}")]
    [Authorize(Roles = nameof(UserRole.Admin))]
    public async Task<ActionResult<ApiResponse<ContentResponseDTO>>> Update(Guid id, [FromBody] ContentUpdateDTO dto)
    {
        var content = await _service.UpdateAsync(id, dto);
        if (content == null)
            return NotFound(new ApiErrorResponse(false, $"Conteúdo com ID '{id}' não encontrado.", null));

        return Ok(new ApiResponse<ContentResponseDTO>(true, "Conteúdo atualizado com sucesso.", content));
    }

    /// <summary>
    /// Remove conteúdo de bem-estar. Requer perfil Admin.
    /// </summary>
    [HttpDelete("{id:guid}")]
    [Authorize(Roles = nameof(UserRole.Admin))]
    public async Task<ActionResult<ApiErrorResponse>> Delete(Guid id)
    {
        var deleted = await _service.DeleteAsync(id);
        if (!deleted)
            return NotFound(new ApiErrorResponse(false, $"Conteúdo com ID '{id}' não encontrado.", null));

        return Ok(new ApiErrorResponse(true, "Conteúdo removido com sucesso.", null));
    }
}
