using CarePlus.MindfulnessAPI.Security;

namespace CarePlus.MindfulnessAPI.Tests.Unit;

public class BCryptPasswordHasherServiceTests
{
    [Fact]
    public void Hash_ShouldCreateNonPlainTextHash_AndVerifyOriginalPassword()
    {
        var hasher = new BCryptPasswordHasherService();
        const string password = "Senha123";

        var hash = hasher.Hash(password);

        Assert.NotEqual(password, hash);
        Assert.True(hasher.Verify(password, hash));
        Assert.False(hasher.Verify("SenhaErrada123", hash));
    }
}
