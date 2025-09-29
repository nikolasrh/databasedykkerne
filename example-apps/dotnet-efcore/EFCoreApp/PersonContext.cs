using Microsoft.EntityFrameworkCore;

namespace EFCoreApp;

public class PersonContext : DbContext
{
    public PersonContext()
    {
    }
    public PersonContext(DbContextOptions<PersonContext> options) : base(options)
    {
    }

    public DbSet<PersonEntity> TestEntities { get; set; }

    protected override void OnConfiguring(DbContextOptionsBuilder options)
        => options.UseNpgsql($"Host=host.docker.internal;Port=5432;Database=efcore_db;Username=efcore_user;Password=password;");

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
    public int Age { get; set; } = 3;
}
