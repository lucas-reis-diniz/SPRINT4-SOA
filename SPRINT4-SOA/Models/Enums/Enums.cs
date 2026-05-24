namespace CarePlus.MindfulnessAPI.Models.Enums;

public enum MoodLevel
{
    MuitoBaixo = 1,
    Baixo = 2,
    Neutro = 3,
    Bom = 4,
    Excelente = 5
}

public enum SessionType
{
    Meditacao,
    Respiracao,
    BodyScan,
    Visualizacao,
    Relaxamento
}

public enum ContentCategory
{
    Artigo,
    Audio,
    Video,
    Exercicio,
    Dica
}

public enum UserRole
{
    User,
    Admin
}
