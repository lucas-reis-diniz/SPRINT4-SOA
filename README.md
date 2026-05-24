# CarePlus Mindfulness API

**Sprint 4 — Arquitetura Orientada a Serviços e Web Services**

## Descrição do projeto

A **CarePlus Mindfulness API** é uma API RESTful desenvolvida em **ASP.NET Core 8** para gerenciamento de recursos digitais voltados ao bem-estar, saúde mental preventiva e práticas de mindfulness. O sistema permite administrar usuários, sessões de meditação, registros de humor e conteúdos de bem-estar, mantendo uma estrutura organizada em camadas e alinhada às boas práticas de desenvolvimento orientado a objetos.

Nesta Sprint 4, o projeto foi evoluído para implementar **autenticação e autorização seguras**, uso de **JWT**, armazenamento de senhas com **BCrypt**, documentação automática da API com **Swagger/OpenAPI**, regras de negócio encapsuladas em services, aplicação dos princípios **SOLID** e testes automatizados unitários e de integração.

## Tecnologias utilizadas

| Tecnologia | Finalidade |
|---|---|
| ASP.NET Core 8 | Desenvolvimento da API RESTful. |
| Entity Framework Core | Mapeamento objeto-relacional e acesso ao banco de dados. |
| PostgreSQL | Banco de dados relacional utilizado pela aplicação. |
| JWT Bearer Authentication | Autenticação stateless e autorização por token. |
| BCrypt.Net-Next | Criptografia segura das senhas dos usuários. |
| Swagger / OpenAPI | Documentação automática e interativa dos endpoints. |
| xUnit | Criação dos testes automatizados. |
| Moq | Criação de mocks para testes unitários. |

## Funcionalidades implementadas

| Módulo | Funcionalidades |
|---|---|
| Autenticação | Registro de usuário, login e geração de token JWT. |
| Usuários | Cadastro, consulta, atualização e exclusão de usuários. |
| Sessões de meditação | Registro, consulta, atualização e exclusão de sessões. |
| Registros de humor | Cadastro e acompanhamento de registros de humor dos usuários. |
| Conteúdos de bem-estar | Cadastro, consulta, atualização e exclusão de conteúdos. |
| Segurança | Autorização por perfil, autenticação stateless e senhas com BCrypt. |
| Documentação | Endpoints documentados automaticamente no Swagger. |
| Testes | Testes unitários e de integração para services e endpoints da API. |

## Arquitetura do projeto

O projeto segue uma arquitetura em camadas, separando responsabilidades de forma clara. Os **controllers** são responsáveis por receber as requisições HTTP e devolver respostas padronizadas. Os **services** concentram as regras de negócio da aplicação. Os **repositories** encapsulam o acesso ao banco de dados. Os **DTOs** definem os dados de entrada e saída da API, evitando exposição direta das entidades de domínio.

```text
Cliente / Swagger
        |
        v
Controllers
        |
        v
Services
        |
        v
Repositories
        |
        v
PostgreSQL
```

## Segurança e autenticação

A aplicação utiliza autenticação **stateless** com **JWT**, ou seja, o servidor não mantém sessão do usuário. Após o login, a API retorna um token que deve ser enviado nas próximas requisições protegidas por meio do cabeçalho `Authorization`.

```http
Authorization: Bearer seu_token_jwt
```

As senhas são armazenadas utilizando **BCrypt**, garantindo que nenhuma senha seja salva em texto puro no banco de dados. Além disso, a API possui autorização por perfil, permitindo restringir determinados endpoints a usuários administradores.

## Documentação da API

A documentação automática pode ser acessada pelo Swagger após executar a aplicação. O Swagger permite visualizar os endpoints, os modelos de requisição e resposta, além de testar chamadas diretamente pelo navegador.

```text
https://localhost:5001/swagger
```

ou, conforme a porta configurada localmente:

```text
http://localhost:5000/swagger
```

## Como executar o projeto

Clone o repositório:

```bash
git clone https://github.com/lucas-reis-diniz/SPRINT3-SOA.git
cd SPRINT3-SOA
```

Restaure as dependências:

```bash
dotnet restore
```

Configure a conexão com o banco de dados no arquivo `appsettings.json`:

```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Host=localhost;Port=5432;Database=careplus_mindfulness;Username=postgres;Password=postgres"
  }
}
```

Aplique as migrations no banco de dados:

```bash
dotnet ef database update
```

Execute a aplicação:

```bash
dotnet run
```

## Como executar os testes

Para executar os testes automatizados, utilize o comando:

```bash
dotnet test CarePlus.MindfulnessAPI.Tests/CarePlus.MindfulnessAPI.Tests.csproj
```

A validação final da Sprint 4 foi realizada com sucesso, apresentando build sem erros e testes automatizados aprovados.

| Validação | Resultado |
|---|---:|
| Build do projeto | Aprovado |
| Testes executados | 11 |
| Testes aprovados | 11 |
| Testes com falha | 0 |

## Critérios da Sprint 4 atendidos

| Critério | Implementação no projeto |
|---|---|
| Estruturação do projeto e código limpo | Separação em controllers, services, repositories, DTOs, security e mapping. |
| Princípios SOLID | Uso de interfaces, injeção de dependência e separação de responsabilidades. |
| Segurança e autenticação | JWT, BCrypt, autorização por perfil e configuração stateless. |
| Regras de negócio como serviços | Lógicas e validações implementadas na camada de services. |
| Documentação automática | Swagger/OpenAPI configurado para documentar os endpoints. |
| Testes automatizados | Testes unitários e de integração implementados com xUnit. |
| Documentação do projeto | README com descrição, execução, testes, tecnologias e integrantes. |

## Integrantes do grupo

| Nome | RM |
|---|---:|
| Diana Letícia de Souza Inocencio | 553562 |
| João Viktor Carvalho de Souza | 552613 |
| Lucas Reis Diniz | 552838 |
| Thiago Araújo Vieira | 553477 |
| Victor Augusto Pereira dos Santos | 553518 |
| Vitor de Moura Nascimento | 553806 |

## Repositório

O código-fonte do projeto está disponível no GitHub:

```text
https://github.com/lucas-reis-diniz/SPRINT3-SOA
```

## Licença

Este projeto foi desenvolvido para fins acadêmicos, como parte da entrega da Sprint 4 da disciplina **Arquitetura Orientada a Serviços e Web Services**.
