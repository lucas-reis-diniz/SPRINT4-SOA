from pathlib import Path
root = Path('/home/ubuntu/SPRINT3-SOA')

def write(relative, content):
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')

write('Middleware/GlobalExceptionMiddleware.cs', r'''using System.Net;
using System.Text.Json;
using CarePlus.MindfulnessAPI.Models.DTOs;

namespace CarePlus.MindfulnessAPI.Middleware;

public class GlobalExceptionMiddleware
{
    private readonly RequestDelegate _next;
    private readonly ILogger<GlobalExceptionMiddleware> _logger;

    public GlobalExceptionMiddleware(RequestDelegate next, ILogger<GlobalExceptionMiddleware> logger)
    {
        _next = next;
        _logger = logger;
    }

    public async Task InvokeAsync(HttpContext context)
    {
        try
        {
            await _next(context);
        }
        catch (UnauthorizedAccessException ex)
        {
            _logger.LogWarning(ex, "Falha de autenticação: {Message}", ex.Message);
            await HandleExceptionAsync(context, HttpStatusCode.Unauthorized, ex.Message);
        }
        catch (InvalidOperationException ex)
        {
            _logger.LogWarning(ex, "Erro de validação: {Message}", ex.Message);
            await HandleExceptionAsync(context, HttpStatusCode.BadRequest, ex.Message);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Erro interno não tratado: {Message}", ex.Message);
            await HandleExceptionAsync(context, HttpStatusCode.InternalServerError,
                "Ocorreu um erro interno no servidor. Tente novamente mais tarde.");
        }
    }

    private static async Task HandleExceptionAsync(HttpContext context, HttpStatusCode statusCode, string message)
    {
        context.Response.ContentType = "application/json";
        context.Response.StatusCode = (int)statusCode;

        var response = new ApiErrorResponse(false, message, null);
        var json = JsonSerializer.Serialize(response, new JsonSerializerOptions
        {
            PropertyNamingPolicy = JsonNamingPolicy.CamelCase
        });

        await context.Response.WriteAsync(json);
    }
}
''')

write('Controllers/UsersController.cs', r'''using CarePlus.MindfulnessAPI.Models.DTOs;
using CarePlus.MindfulnessAPI.Models.Enums;
using CarePlus.MindfulnessAPI.Services.Interfaces;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace CarePlus.MindfulnessAPI.Controllers;

[ApiController]
[Route("api/[controller]")]
[Authorize(Roles = nameof(UserRole.Admin))]
public class UsersController : ControllerBase
{
    private readonly IUserService _service;

    public UsersController(IUserService service)
    {
        _service = service;
    }

    /// <summary>
    /// Retorna todos os usuários cadastrados. Requer perfil Admin.
    /// </summary>
    [HttpGet]
    public async Task<ActionResult<ApiResponse<IEnumerable<UserResponseDTO>>>> GetAll()
    {
        var users = await _service.GetAllAsync();
        return Ok(new ApiResponse<IEnumerable<UserResponseDTO>>(true, "Usuários listados com sucesso.", users));
    }

    /// <summary>
    /// Retorna um usuário pelo ID. Requer perfil Admin.
    /// </summary>
    [HttpGet("{id:guid}")]
    public async Task<ActionResult<ApiResponse<UserResponseDTO>>> GetById(Guid id)
    {
        var user = await _service.GetByIdAsync(id);
        if (user == null)
            return NotFound(new ApiErrorResponse(false, $"Usuário com ID '{id}' não encontrado.", null));

        return Ok(new ApiResponse<UserResponseDTO>(true, "Usuário encontrado.", user));
    }

    /// <summary>
    /// Cadastra um usuário com perfil definido. Requer perfil Admin.
    /// </summary>
    [HttpPost]
    public async Task<ActionResult<ApiResponse<UserResponseDTO>>> Create([FromBody] UserCreateDTO dto)
    {
        var user = await _service.CreateAsync(dto);
        return CreatedAtAction(nameof(GetById), new { id = user.Id },
            new ApiResponse<UserResponseDTO>(true, "Usuário criado com sucesso.", user));
    }

    /// <summary>
    /// Atualiza dados cadastrais e perfil de um usuário. Requer perfil Admin.
    /// </summary>
    [HttpPut("{id:guid}")]
    public async Task<ActionResult<ApiResponse<UserResponseDTO>>> Update(Guid id, [FromBody] UserUpdateDTO dto)
    {
        var user = await _service.UpdateAsync(id, dto);
        if (user == null)
            return NotFound(new ApiErrorResponse(false, $"Usuário com ID '{id}' não encontrado.", null));

        return Ok(new ApiResponse<UserResponseDTO>(true, "Usuário atualizado com sucesso.", user));
    }

    /// <summary>
    /// Remove um usuário pelo ID. Requer perfil Admin.
    /// </summary>
    [HttpDelete("{id:guid}")]
    public async Task<ActionResult<ApiErrorResponse>> Delete(Guid id)
    {
        var deleted = await _service.DeleteAsync(id);
        if (!deleted)
            return NotFound(new ApiErrorResponse(false, $"Usuário com ID '{id}' não encontrado.", null));

        return Ok(new ApiErrorResponse(true, "Usuário removido com sucesso.", null));
    }
}
''')

write('Controllers/MeditationSessionsController.cs', r'''using CarePlus.MindfulnessAPI.Models.DTOs;
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
''')

write('Controllers/MoodEntriesController.cs', r'''using CarePlus.MindfulnessAPI.Models.DTOs;
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
''')

write('Controllers/WellnessContentsController.cs', r'''using CarePlus.MindfulnessAPI.Models.DTOs;
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
''')

print('Controllers protegidos e middleware ajustado.')
