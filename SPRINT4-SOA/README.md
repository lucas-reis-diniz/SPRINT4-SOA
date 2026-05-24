# CarePlus Mindfulness API

**CarePlus Mindfulness API** é uma API RESTful para apoio à saúde mental preventiva e práticas de mindfulness, desenvolvida como entrega acadêmica da disciplina **Arquitetura Orientada a Serviços e Web Services — Sprint 4**. O projeto foi evoluído a partir da Sprint 3 para contemplar autenticação e autorização seguras, boas práticas de orientação a objetos, documentação OpenAPI/Swagger e testes automatizados.

> A aplicação segue uma arquitetura em camadas, na qual controllers expõem os recursos HTTP, services concentram regras de negócio, repositories abstraem o acesso a dados e DTOs protegem o contrato público da API.

## Descrição do projeto

A API permite gerenciar usuários, sessões de meditação, registros de humor e conteúdos de bem-estar. A proposta é apoiar beneficiários em uma experiência digital de autocuidado, sem atuar como diagnóstico clínico ou telemedicina. A evolução da Sprint 4 acrescentou **segurança stateless com JWT**, armazenamento de senhas com **BCrypt**, autorização por perfil, tratamento global de erros, mapeadores por interface, validações nos services e testes unitários e de integração.

O projeto utiliza **ASP.NET Core 8**, framework oficial da Microsoft para APIs web modernas, e expõe documentação interativa com **Swagger/OpenAPI**, padrão amplamente usado para descrição e consumo de APIs REST.[1] [2] O acesso a dados é implementado com **Entity Framework Core**, ORM que permite mapear entidades .NET para bancos relacionais, e o banco configurado é **PostgreSQL** por meio do provider Npgsql.[3] [4]

## Tecnologias utilizadas

| Tecnologia | Versão utilizada | Finalidade no projeto |
|---|---:|---|
| .NET SDK | 8.0 | Plataforma de desenvolvimento e execução da API. |
| ASP.NET Core Web API | 8.0 | Exposição dos endpoints REST, middleware e autenticação. |
| Entity Framework Core | 8.0.8 | Mapeamento objeto-relacional e acesso ao banco. |
| Npgsql Entity Framework Core Provider | 8.0.8 | Integração entre EF Core e PostgreSQL. |
| PostgreSQL | 16 ou superior recomendado | Banco de dados relacional da aplicação. |
| Swashbuckle.AspNetCore | 6.5.0 | Geração automática da documentação Swagger/OpenAPI. |
| Microsoft.AspNetCore.Authentication.JwtBearer | 8.0.8 | Validação de tokens JWT nas requisições protegidas. |
| BCrypt.Net-Next | 4.0.3 | Hash seguro das senhas dos usuários. |
| xUnit, Moq e WebApplicationFactory | Conforme `CarePlus.MindfulnessAPI.Tests.csproj` | Testes unitários, mocks e testes de integração da API. |

## Funcionalidades principais

| Área | Funcionalidade | Controle de acesso |
|---|---|---|
| Autenticação | Registro e login com geração de token JWT. | Público. |
| Usuários | Cadastro, consulta, atualização e exclusão de usuários. | Administração para listagem, criação, atualização e exclusão; leitura do próprio perfil permitida ao usuário autenticado. |
| Sessões de meditação | Registro, consulta, atualização e exclusão de sessões. | Usuário autenticado; exclusão restrita a administrador. |
| Registros de humor | Registro, consulta, atualização e exclusão de humor diário. | Usuário autenticado; exclusão restrita a administrador. |
| Conteúdos de bem-estar | Consulta de conteúdos ativos, cadastro, atualização e exclusão. | Consulta pública para conteúdos ativos; manutenção restrita a administrador. |
| Documentação | Interface Swagger com autenticação Bearer. | Disponível em ambiente de desenvolvimento. |

## Arquitetura e organização

A aplicação foi organizada para atender aos critérios de código limpo, modularização e princípios SOLID. Os controllers não concentram regras de negócio; eles apenas recebem requisições, acionam interfaces de service e retornam respostas padronizadas. As regras de validação e criação de entidades ficam nos services, enquanto a persistência é encapsulada nos repositories.

```text
Cliente HTTP ou Swagger
        |
        v
Controllers
        |
        v
Interfaces de Services
        |
        v
Services de negócio + mapeadores + validações
        |
        v
Interfaces de Repositories
        |
        v
Repositories EF Core
        |
        v
PostgreSQL
```

| Pasta ou arquivo | Responsabilidade |
|---|---|
| `Controllers/` | Define os endpoints HTTP e as respostas da API. |
| `Services/` | Contém as regras de negócio e orquestra o uso dos repositories. |
| `Services/Interfaces/` | Expõe contratos usados pelos controllers, favorecendo inversão de dependência. |
| `Repositories/` | Implementa o acesso a dados com Entity Framework Core. |
| `Repositories/Interfaces/` | Define contratos de persistência usados pelos services. |
| `Models/Entities/` | Representa as entidades do domínio persistidas no banco. |
| `Models/DTOs/` | Define objetos de entrada e saída da API. |
| `Models/Enums/` | Centraliza enums de perfil, humor, tipo de sessão e categorias. |
| `Security/` | Implementa hashing BCrypt, geração de JWT e política de senha. |
| `Security/Interfaces/` | Define contratos de segurança para inversão de dependência. |
| `Mapping/` | Contém mapeadores de entidades para DTOs. |
| `Middleware/` | Implementa tratamento global de exceções. |
| `Data/AppDbContext.cs` | Configura o EF Core, relacionamentos, conversões e seed data. |
| `CarePlus.MindfulnessAPI.Tests/` | Contém testes unitários e de integração da Sprint 4. |

## Princípios SOLID aplicados

A evolução da Sprint 4 reforçou a separação de responsabilidades e o uso de abstrações. Services dependem de interfaces de repositories, controllers dependem de interfaces de services, e componentes de segurança foram separados em contratos próprios. O mapeamento Entity-to-DTO foi extraído para classes específicas, evitando que os services acumulem responsabilidades de apresentação.

| Princípio | Aplicação no projeto |
|---|---|
| **Single Responsibility Principle** | Controllers tratam HTTP, services tratam regras de negócio, repositories tratam persistência, mappers tratam conversão de modelos e classes de segurança tratam autenticação. |
| **Open/Closed Principle** | Novas implementações de mapeadores, hashing, token ou repositories podem ser adicionadas por interfaces sem alterar controllers. |
| **Liskov Substitution Principle** | Classes concretas podem ser substituídas por implementações dos contratos `IUserRepository`, `IAuthService`, `IPasswordHasherService`, `IJwtTokenService` e `IModelMapper`. |
| **Interface Segregation Principle** | Contratos são específicos para cada domínio, como `IUserService`, `IMoodEntryService`, `IWellnessContentRepository` e `IPasswordPolicy`. |
| **Dependency Inversion Principle** | Camadas de alto nível dependem de abstrações registradas no contêiner de injeção de dependência do ASP.NET Core. |

## Segurança, autenticação e autorização

A API usa autenticação **stateless** com tokens JWT. Depois do login ou registro, o cliente recebe um token assinado e deve enviá-lo no cabeçalho `Authorization` das chamadas protegidas. Essa abordagem evita manter sessão no servidor e é adequada para APIs REST que precisam escalar horizontalmente.[5]

```http
Authorization: Bearer {seu_token_jwt}
```

As senhas não são persistidas em texto puro. O projeto usa BCrypt para gerar hashes com salt, evitando a comparação direta com o valor informado pelo usuário. A política de senha exige pelo menos oito caracteres e combinação de letras e números. A autorização é baseada em perfis, com os papéis `User` e `Admin`.

| Recurso de segurança | Implementação |
|---|---|
| Autenticação stateless | `AddAuthentication().AddJwtBearer(...)` em `Program.cs`. |
| Geração de token | `JwtTokenService`, com issuer, audience, chave e expiração configuráveis. |
| Hash de senha | `BCryptPasswordHasherService`. |
| Política de senha | `DefaultPasswordPolicy`, registrada via `IPasswordPolicy`. |
| Perfis | Enum `UserRole` com `User` e `Admin`. |
| Filtro de requisições | Middleware JWT Bearer do ASP.NET Core antes da autorização. |
| Autorização por endpoint | Atributos `[Authorize]` e `[Authorize(Roles = "Admin")]`. |
| Tratamento de erros | `GlobalExceptionMiddleware`, com respostas padronizadas. |

## Endpoints da API

A tabela abaixo resume os principais endpoints. A documentação completa, com exemplos e esquemas dos DTOs, pode ser acessada pelo Swagger quando a aplicação estiver em execução.

| Grupo | Método | Rota | Descrição | Acesso |
|---|---|---|---|---|
| Autenticação | `POST` | `/api/Auth/register` | Registra usuário comum e retorna token JWT. | Público |
| Autenticação | `POST` | `/api/Auth/login` | Autentica credenciais e retorna token JWT. | Público |
| Usuários | `GET` | `/api/Users` | Lista todos os usuários. | Admin |
| Usuários | `GET` | `/api/Users/{id}` | Busca usuário por ID. | Autenticado, com regra de escopo aplicada no controller |
| Usuários | `POST` | `/api/Users` | Cria usuário com perfil indicado no DTO. | Admin |
| Usuários | `PUT` | `/api/Users/{id}` | Atualiza usuário. | Admin |
| Usuários | `DELETE` | `/api/Users/{id}` | Remove usuário. | Admin |
| Sessões | `GET` | `/api/MeditationSessions` | Lista sessões. | Autenticado |
| Sessões | `GET` | `/api/MeditationSessions/{id}` | Busca sessão por ID. | Autenticado |
| Sessões | `GET` | `/api/MeditationSessions/user/{userId}` | Lista sessões de um usuário. | Autenticado |
| Sessões | `POST` | `/api/MeditationSessions` | Cria sessão de meditação. | Autenticado |
| Sessões | `PUT` | `/api/MeditationSessions/{id}` | Atualiza sessão. | Autenticado |
| Sessões | `DELETE` | `/api/MeditationSessions/{id}` | Remove sessão. | Admin |
| Humor | `GET` | `/api/MoodEntries` | Lista registros de humor. | Autenticado |
| Humor | `GET` | `/api/MoodEntries/{id}` | Busca registro por ID. | Autenticado |
| Humor | `GET` | `/api/MoodEntries/user/{userId}` | Lista registros por usuário. | Autenticado |
| Humor | `POST` | `/api/MoodEntries` | Cria registro de humor. | Autenticado |
| Humor | `PUT` | `/api/MoodEntries/{id}` | Atualiza registro de humor. | Autenticado |
| Humor | `DELETE` | `/api/MoodEntries/{id}` | Remove registro de humor. | Admin |
| Conteúdos | `GET` | `/api/WellnessContents/active` | Lista conteúdos ativos. | Público |
| Conteúdos | `GET` | `/api/WellnessContents` | Lista todos os conteúdos. | Autenticado |
| Conteúdos | `GET` | `/api/WellnessContents/{id}` | Busca conteúdo por ID. | Público |
| Conteúdos | `POST` | `/api/WellnessContents` | Cria conteúdo. | Admin |
| Conteúdos | `PUT` | `/api/WellnessContents/{id}` | Atualiza conteúdo. | Admin |
| Conteúdos | `DELETE` | `/api/WellnessContents/{id}` | Remove conteúdo. | Admin |

## Pré-requisitos

Antes de executar a API, instale o SDK do .NET 8 e mantenha um servidor PostgreSQL disponível. O Entity Framework Core CLI é necessário apenas se você for criar ou aplicar migrations manualmente.

| Dependência | Verificação sugerida |
|---|---|
| .NET SDK 8 | `dotnet --version` |
| PostgreSQL | `psql --version` |
| EF Core CLI | `dotnet ef --version` |

Caso o EF Core CLI não esteja instalado, execute:

```bash
dotnet tool install --global dotnet-ef
```

## Como executar a aplicação

Clone o repositório e entre na pasta do projeto:

```bash
git clone https://github.com/lucas-reis-diniz/SPRINT3-SOA.git
cd SPRINT3-SOA
```

Restaure as dependências:

```bash
dotnet restore
```

Configure o arquivo `appsettings.json` com os dados do PostgreSQL. O exemplo abaixo usa os valores locais presentes no projeto, mas a senha deve ser ajustada conforme seu ambiente.

```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Host=localhost;Port=5432;Database=careplus_mindfulness;Username=postgres;Password=postgres"
  },
  "Jwt": {
    "Issuer": "CarePlus.MindfulnessAPI",
    "Audience": "CarePlus.MindfulnessAPI.Client",
    "Key": "CarePlus-Sprint4-Development-Key-Change-In-Production-2026",
    "ExpirationMinutes": 120
  }
}
```

Crie a migration inicial, se ainda não existir no ambiente local, e aplique a estrutura no banco:

```bash
dotnet ef migrations add InitialCreate
dotnet ef database update
```

Execute a aplicação:

```bash
dotnet run
```

Em ambiente de desenvolvimento, a documentação interativa estará disponível em:

```text
https://localhost:5001/swagger
http://localhost:5000/swagger
```

A URL exata pode variar conforme o perfil de execução do ASP.NET Core. Verifique o terminal após o comando `dotnet run`.

## Como usar a autenticação

Primeiro registre um usuário comum ou faça login com um usuário existente. Em seguida, copie o token retornado e informe no Swagger pelo botão **Authorize**, usando o formato `Bearer {token}`.

### Registro de usuário

```http
POST /api/Auth/register
Content-Type: application/json
```

```json
{
  "nome": "Ana Costa",
  "email": "ana.costa@email.com",
  "senha": "Senha123",
  "dataNascimento": "1995-03-20"
}
```

Resposta esperada:

```json
{
  "sucesso": true,
  "mensagem": "Usuário registrado com sucesso.",
  "dados": {
    "token": "eyJhbGciOi...",
    "expiresAt": "2026-05-24T23:00:00Z",
    "usuario": {
      "id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
      "nome": "Ana Costa",
      "email": "ana.costa@email.com",
      "role": "User"
    }
  }
}
```

### Login

```http
POST /api/Auth/login
Content-Type: application/json
```

```json
{
  "email": "admin@careplus.com",
  "senha": "Admin123"
}
```

> O banco possui dados iniciais para desenvolvimento. Caso o hash de senha seedado seja alterado, gere novamente os dados ou cadastre usuários por meio dos endpoints da API.

## Documentação Swagger/OpenAPI

A documentação automática é configurada em `Program.cs` com `AddSwaggerGen`. A configuração inclui título, versão, descrição, leitura de comentários XML e suporte ao esquema de segurança **Bearer JWT**. O Swagger permite testar endpoints públicos e protegidos diretamente pelo navegador, desde que o token seja informado no campo de autorização.

| Item documentado | Situação |
|---|---|
| Título e versão da API | Configurado em `OpenApiInfo`. |
| Segurança JWT | Configurada por `AddSecurityDefinition` e `AddSecurityRequirement`. |
| DTOs de entrada e saída | Exibidos automaticamente pelo Swashbuckle. |
| Endpoints agrupados por controller | Disponíveis na interface Swagger UI. |
| Comentários XML | Habilitados por `GenerateDocumentationFile` no `.csproj`. |

## Como rodar os testes

A Sprint 4 inclui um projeto de testes separado em `CarePlus.MindfulnessAPI.Tests`. A suíte cobre regras de senha, hashing BCrypt, service de usuário, autenticação, autorização e chamadas de integração contra uma aplicação em memória por meio de `WebApplicationFactory`.

Execute todos os testes com:

```bash
dotnet test CarePlus.MindfulnessAPI.Tests/CarePlus.MindfulnessAPI.Tests.csproj
```

Para gerar um arquivo TRX com o resultado:

```bash
dotnet test CarePlus.MindfulnessAPI.Tests/CarePlus.MindfulnessAPI.Tests.csproj --logger "trx;LogFileName=sprint4-tests.trx"
```

Resultado validado nesta entrega:

| Métrica | Resultado |
|---|---:|
| Total de testes | 11 |
| Testes aprovados | 11 |
| Testes falhos | 0 |
| Testes ignorados | 0 |

## Boas práticas implementadas na Sprint 4

| Critério da Sprint 4 | Implementação realizada |
|---|---|
| Estruturação do projeto e código limpo | Camadas claras, DTOs, repositories, services, mappers e interfaces. |
| Interfaces, polimorfismo e despacho dinâmico | Injeção de dependência por contratos em services, repositories, segurança e mapeamento. |
| Separação de responsabilidades | Controllers não acessam diretamente o banco; regras ficam nos services; persistência fica nos repositories. |
| Princípios SOLID | Componentes menores, substituíveis e com responsabilidades específicas. |
| Segurança stateless | JWT Bearer configurado sem sessão de servidor. |
| BCrypt | Hash e verificação de senha por `BCryptPasswordHasherService`. |
| Filtros de requisição | Middleware de autenticação JWT e autorização do ASP.NET Core. |
| Autorização por perfil | Uso de `UserRole`, claims e atributos `[Authorize]`. |
| Regras como serviços | Validações de usuário, senha, sessão, humor e conteúdo nos services. |
| Swagger/OpenAPI | Interface interativa com suporte a Bearer Token. |
| Testes automatizados | xUnit, Moq, EF Core InMemory e WebApplicationFactory. |
| Documentação do projeto | README atualizado com execução, testes, endpoints, segurança e tecnologias. |

## Respostas padronizadas

A API utiliza o DTO `ApiResponse<T>` para manter consistência entre respostas de sucesso e erro. Exemplo de erro tratado pelo middleware global:

```json
{
  "sucesso": false,
  "mensagem": "E-mail ou senha inválidos.",
  "dados": null
}
```

Esse padrão facilita o consumo da API por clientes web ou mobile, pois o formato da resposta permanece previsível.

## Autores

| Nome | RM |
|---|---:|
| Diana Letícia de Souza Inocencio | 553562 |
| João Viktor Carvalho de Souza | 552613 |
| Lucas Reis Diniz | 552838 |
| Thiago Araújo Vieira | 553477 |
| Victor Augusto Pereira dos Santos | 553518 |
| Vitor de Moura Nascimento | 553806 |

Turma: Engenharia de Software — 3º ano. Instituição: FIAP. Ano: 2025.

## Licença

Este projeto é parte de uma entrega acadêmica do Challenge Care Plus — FIAP 2025. O uso, reprodução e avaliação devem seguir as regras da disciplina e da instituição.

## Referências

[1]: https://learn.microsoft.com/aspnet/core/web-api/ "Microsoft Learn — Create web APIs with ASP.NET Core"
[2]: https://swagger.io/specification/ "OpenAPI Initiative — OpenAPI Specification"
[3]: https://learn.microsoft.com/ef/core/ "Microsoft Learn — Entity Framework Core"
[4]: https://www.npgsql.org/efcore/ "Npgsql — Entity Framework Core Provider"
[5]: https://learn.microsoft.com/aspnet/core/security/authentication/configure-jwt-bearer-authentication "Microsoft Learn — Configure JWT bearer authentication in ASP.NET Core"
