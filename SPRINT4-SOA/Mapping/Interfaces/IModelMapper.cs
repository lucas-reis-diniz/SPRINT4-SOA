namespace CarePlus.MindfulnessAPI.Mapping.Interfaces;

public interface IModelMapper<in TSource, out TDestination>
{
    TDestination Map(TSource source);
}
