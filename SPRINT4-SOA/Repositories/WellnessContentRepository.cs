using CarePlus.MindfulnessAPI.Data;
using CarePlus.MindfulnessAPI.Models.Entities;
using CarePlus.MindfulnessAPI.Repositories.Interfaces;
using Microsoft.EntityFrameworkCore;

namespace CarePlus.MindfulnessAPI.Repositories;

public class WellnessContentRepository : IWellnessContentRepository
{
    private readonly AppDbContext _context;

    public WellnessContentRepository(AppDbContext context)
    {
        _context = context;
    }

    public async Task<IEnumerable<WellnessContent>> GetAllAsync()
    {
        return await _context.WellnessContents
            .AsNoTracking()
            .OrderByDescending(c => c.CriadoEm)
            .ToListAsync();
    }

    public async Task<IEnumerable<WellnessContent>> GetActiveAsync()
    {
        return await _context.WellnessContents
            .Where(c => c.Ativo)
            .AsNoTracking()
            .OrderByDescending(c => c.CriadoEm)
            .ToListAsync();
    }

    public async Task<WellnessContent?> GetByIdAsync(Guid id)
    {
        return await _context.WellnessContents.FindAsync(id);
    }

    public async Task<WellnessContent> CreateAsync(WellnessContent content)
    {
        _context.WellnessContents.Add(content);
        await _context.SaveChangesAsync();
        return content;
    }

    public async Task<WellnessContent> UpdateAsync(WellnessContent content)
    {
        content.AtualizadoEm = DateTime.UtcNow;
        _context.WellnessContents.Update(content);
        await _context.SaveChangesAsync();
        return content;
    }

    public async Task<bool> DeleteAsync(Guid id)
    {
        var content = await _context.WellnessContents.FindAsync(id);
        if (content == null) return false;

        _context.WellnessContents.Remove(content);
        await _context.SaveChangesAsync();
        return true;
    }
}
