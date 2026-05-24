using CarePlus.MindfulnessAPI.Data;
using CarePlus.MindfulnessAPI.Models.Entities;
using CarePlus.MindfulnessAPI.Repositories.Interfaces;
using Microsoft.EntityFrameworkCore;

namespace CarePlus.MindfulnessAPI.Repositories;

public class MeditationSessionRepository : IMeditationSessionRepository
{
    private readonly AppDbContext _context;

    public MeditationSessionRepository(AppDbContext context)
    {
        _context = context;
    }

    public async Task<IEnumerable<MeditationSession>> GetAllAsync()
    {
        return await _context.MeditationSessions
            .Include(s => s.User)
            .AsNoTracking()
            .OrderByDescending(s => s.RealizadaEm)
            .ToListAsync();
    }

    public async Task<IEnumerable<MeditationSession>> GetByUserIdAsync(Guid userId)
    {
        return await _context.MeditationSessions
            .Include(s => s.User)
            .Where(s => s.UserId == userId)
            .AsNoTracking()
            .OrderByDescending(s => s.RealizadaEm)
            .ToListAsync();
    }

    public async Task<MeditationSession?> GetByIdAsync(Guid id)
    {
        return await _context.MeditationSessions
            .Include(s => s.User)
            .FirstOrDefaultAsync(s => s.Id == id);
    }

    public async Task<MeditationSession> CreateAsync(MeditationSession session)
    {
        _context.MeditationSessions.Add(session);
        await _context.SaveChangesAsync();
        return session;
    }

    public async Task<MeditationSession> UpdateAsync(MeditationSession session)
    {
        _context.MeditationSessions.Update(session);
        await _context.SaveChangesAsync();
        return session;
    }

    public async Task<bool> DeleteAsync(Guid id)
    {
        var session = await _context.MeditationSessions.FindAsync(id);
        if (session == null) return false;

        _context.MeditationSessions.Remove(session);
        await _context.SaveChangesAsync();
        return true;
    }
}
