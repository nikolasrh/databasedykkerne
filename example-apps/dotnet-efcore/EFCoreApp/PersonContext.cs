using Microsoft.EntityFrameworkCore;

namespace EFCoreApp;

public class PersonContext : DbContext
{
    public PersonContext(DbContextOptions<PersonContext> options) : base(options)
    {
    }

    public DbSet<PersonEntity> TestEntities { get; set; }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<PersonEntity>(entity =>
        {
            entity.HasKey(e => e.Id);
            entity.Property(e => e.Name).HasMaxLength(100);
        });
    }
}

public class PersonEntity
{
    public int Id { get; set; }
    public string Name { get; set; } = string.Empty;
}
