using CarePlus.MindfulnessAPI.Data;
using CarePlus.MindfulnessAPI.Models.Entities;
using CarePlus.MindfulnessAPI.Repositories.Interfaces;
using Microsoft.EntityFrameworkCore;

namespace CarePlus.MindfulnessAPI.Repositories;

public class MoodEntryRepository : IMoodEntryRepository
{
    private readonly AppDbContext _context;

    public MoodEntryRepository(AppDbContext context)
    {
        _context = context;
    }

    public async Task<IEnumerable<MoodEntry>> GetAllAsync()
    {
        return await _context.MoodEntries
            .Include(m => m.User)
            .AsNoTracking()
            .OrderByDescending(m => m.DataRegistro)
            .ToListAsync();
    }

    public async Task<IEnumerable<MoodEntry>> GetByUserIdAsync(Guid userId)
    {
        return await _context.MoodEntries
            .Include(m => m.User)
            .Where(m => m.UserId == userId)
            .AsNoTracking()
            .OrderByDescending(m => m.DataRegistro)
            .ToListAsync();
    }

    public async Task<MoodEntry?> GetByIdAsync(Guid id)
    {
        return await _context.MoodEntries
            .Include(m => m.User)
            .FirstOrDefaultAsync(m => m.Id == id);
    }

    public async Task<MoodEntry> CreateAsync(MoodEntry entry)
    {
        _context.MoodEntries.Add(entry);
        await _context.SaveChangesAsync();
        return entry;
    }

    public async Task<MoodEntry> UpdateAsync(MoodEntry entry)
    {
        _context.MoodEntries.Update(entry);
        await _context.SaveChangesAsync();
        return entry;
    }

    public async Task<bool> DeleteAsync(Guid id)
    {
        var entry = await _context.MoodEntries.FindAsync(id);
        if (entry == null) return false;

        _context.MoodEntries.Remove(entry);
        await _context.SaveChangesAsync();
        return true;
    }
}
