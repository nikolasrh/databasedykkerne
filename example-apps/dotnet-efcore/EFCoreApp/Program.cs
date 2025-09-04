using EFCoreApp;

using var context = new PersonContext();

context.Add(new PersonEntity { Name = "John Doe" });
context.SaveChanges();

var persons = context.TestEntities.ToList();
foreach (var person in persons)
{
  Console.WriteLine($"Person ID: {person.Id}, Name: {person.Name}");
}
