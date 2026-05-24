using CarePlus.MindfulnessAPI.Models.DTOs;
using CarePlus.MindfulnessAPI.Services.Interfaces;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace CarePlus.MindfulnessAPI.Controllers;

[ApiController]
[Route("api/[controller]")]
[AllowAnonymous]
public class AuthController : ControllerBase
{
    private readonly IAuthService _authService;

    public AuthController(IAuthService authService)
    {
        _authService = authService;
    }

    /// <summary>
    /// Cadastra um novo usuário comum e retorna um token JWT.
    /// </summary>
    [HttpPost("register")]
    public async Task<ActionResult<ApiResponse<AuthResponseDTO>>> Register([FromBody] RegisterRequestDTO dto)
    {
        var response = await _authService.RegisterAsync(dto);
        return Created(string.Empty, new ApiResponse<AuthResponseDTO>(true, "Usuário registrado com sucesso.", response));
    }

    /// <summary>
    /// Autentica usuário por e-mail e senha e retorna um token JWT.
    /// </summary>
    [HttpPost("login")]
    public async Task<ActionResult<ApiResponse<AuthResponseDTO>>> Login([FromBody] LoginRequestDTO dto)
    {
        var response = await _authService.LoginAsync(dto);
        return Ok(new ApiResponse<AuthResponseDTO>(true, "Login realizado com sucesso.", response));
    }
}
