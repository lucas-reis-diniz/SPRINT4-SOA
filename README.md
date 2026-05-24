Entrega Sprint 4 — SOA e Web Services

Projeto: CarePlus Mindfulness API
Repositório GitHub: https://github.com/lucas-reis-diniz/SPRINT3-SOA

Descrição: API RESTful em ASP.NET Core 8 para gerenciamento de usuários, sessões de meditação, registros de humor e conteúdos de bem-estar. A Sprint 4 implementa autenticação/autorização segura com JWT, senhas com BCrypt, configuração stateless, autorização por perfis, documentação Swagger/OpenAPI, regras de negócio em services, aplicação de princípios SOLID e testes automatizados.

Como executar:
1. Clonar o repositório.
2. Configurar o PostgreSQL no appsettings.json.
3. Executar dotnet restore.
4. Executar dotnet ef database update.
5. Executar dotnet run.
6. Acessar o Swagger em /swagger.

Como rodar os testes:
dotnet test CarePlus.MindfulnessAPI.Tests/CarePlus.MindfulnessAPI.Tests.csproj

Validação realizada:
- Build aprovado sem erros.
- Testes automatizados: 11 aprovados, 0 falhas.

Integrantes:
Diana Letícia de Souza Inocencio — RM553562
João Viktor Carvalho de Souza — RM552613
Lucas Reis Diniz — RM552838
Thiago Araújo Vieira — RM553477
Victor Augusto Pereira dos Santos — RM553518
Vitor de Moura Nascimento — RM553806
