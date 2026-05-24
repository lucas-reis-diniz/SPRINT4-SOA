using CarePlus.MindfulnessAPI.Security;

namespace CarePlus.MindfulnessAPI.Tests.Unit;

public class DefaultPasswordPolicyTests
{
    [Fact]
    public void Validate_WhenPasswordHasLettersAndNumbers_ShouldNotThrow()
    {
        var policy = new DefaultPasswordPolicy();

        var exception = Record.Exception(() => policy.Validate("Senha123"));

        Assert.Null(exception);
    }

    [Theory]
    [InlineData("")]
    [InlineData("1234567")]
    [InlineData("somenteletras")]
    public void Validate_WhenPasswordDoesNotMatchPolicy_ShouldThrow(string password)
    {
        var policy = new DefaultPasswordPolicy();

        Assert.Throws<InvalidOperationException>(() => policy.Validate(password));
    }
}
