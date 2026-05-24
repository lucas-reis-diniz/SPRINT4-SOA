using System;
using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

#pragma warning disable CA1814 // Prefer jagged arrays over multidimensional

namespace CarePlus.MindfulnessAPI.Migrations
{
    /// <inheritdoc />
    public partial class InitialCreate : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.CreateTable(
                name: "users",
                columns: table => new
                {
                    id = table.Column<Guid>(type: "uuid", nullable: false),
                    nome = table.Column<string>(type: "character varying(150)", maxLength: 150, nullable: false),
                    email = table.Column<string>(type: "character varying(200)", maxLength: 200, nullable: false),
                    data_nascimento = table.Column<DateOnly>(type: "date", nullable: true),
                    criado_em = table.Column<DateTime>(type: "timestamp with time zone", nullable: false),
                    atualizado_em = table.Column<DateTime>(type: "timestamp with time zone", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_users", x => x.id);
                });

            migrationBuilder.CreateTable(
                name: "wellness_contents",
                columns: table => new
                {
                    id = table.Column<Guid>(type: "uuid", nullable: false),
                    titulo = table.Column<string>(type: "character varying(200)", maxLength: 200, nullable: false),
                    descricao = table.Column<string>(type: "character varying(2000)", maxLength: 2000, nullable: false),
                    categoria = table.Column<string>(type: "text", nullable: false),
                    url_recurso = table.Column<string>(type: "character varying(500)", maxLength: 500, nullable: true),
                    duracao_estimada_min = table.Column<int>(type: "integer", nullable: true),
                    ativo = table.Column<bool>(type: "boolean", nullable: false),
                    criado_em = table.Column<DateTime>(type: "timestamp with time zone", nullable: false),
                    atualizado_em = table.Column<DateTime>(type: "timestamp with time zone", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_wellness_contents", x => x.id);
                });

            migrationBuilder.CreateTable(
                name: "meditation_sessions",
                columns: table => new
                {
                    id = table.Column<Guid>(type: "uuid", nullable: false),
                    user_id = table.Column<Guid>(type: "uuid", nullable: false),
                    tipo = table.Column<string>(type: "text", nullable: false),
                    titulo = table.Column<string>(type: "character varying(200)", maxLength: 200, nullable: false),
                    duracao_minutos = table.Column<int>(type: "integer", nullable: false),
                    concluida = table.Column<bool>(type: "boolean", nullable: false),
                    observacoes = table.Column<string>(type: "character varying(500)", maxLength: 500, nullable: true),
                    realizada_em = table.Column<DateTime>(type: "timestamp with time zone", nullable: false),
                    criado_em = table.Column<DateTime>(type: "timestamp with time zone", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_meditation_sessions", x => x.id);
                    table.ForeignKey(
                        name: "FK_meditation_sessions_users_user_id",
                        column: x => x.user_id,
                        principalTable: "users",
                        principalColumn: "id",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateTable(
                name: "mood_entries",
                columns: table => new
                {
                    id = table.Column<Guid>(type: "uuid", nullable: false),
                    user_id = table.Column<Guid>(type: "uuid", nullable: false),
                    nivel_humor = table.Column<string>(type: "text", nullable: false),
                    notas = table.Column<string>(type: "character varying(500)", maxLength: 500, nullable: true),
                    data_registro = table.Column<DateTime>(type: "timestamp with time zone", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_mood_entries", x => x.id);
                    table.ForeignKey(
                        name: "FK_mood_entries_users_user_id",
                        column: x => x.user_id,
                        principalTable: "users",
                        principalColumn: "id",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.InsertData(
                table: "users",
                columns: new[] { "id", "atualizado_em", "criado_em", "data_nascimento", "email", "nome" },
                values: new object[,]
                {
                    { new Guid("a1b2c3d4-e5f6-7890-abcd-ef1234567890"), new DateTime(2025, 1, 1, 0, 0, 0, 0, DateTimeKind.Utc), new DateTime(2025, 1, 1, 0, 0, 0, 0, DateTimeKind.Utc), new DateOnly(1990, 5, 15), "maria.silva@careplus.com", "Maria Silva" },
                    { new Guid("b2c3d4e5-f6a7-8901-bcde-f12345678901"), new DateTime(2025, 1, 1, 0, 0, 0, 0, DateTimeKind.Utc), new DateTime(2025, 1, 1, 0, 0, 0, 0, DateTimeKind.Utc), new DateOnly(1985, 8, 22), "joao.santos@careplus.com", "João Santos" }
                });

            migrationBuilder.InsertData(
                table: "wellness_contents",
                columns: new[] { "id", "ativo", "atualizado_em", "categoria", "criado_em", "descricao", "duracao_estimada_min", "titulo", "url_recurso" },
                values: new object[,]
                {
                    { new Guid("c3d4e5f6-a7b8-9012-cdef-123456789012"), true, new DateTime(2025, 1, 1, 0, 0, 0, 0, DateTimeKind.Utc), "Artigo", new DateTime(2025, 1, 1, 0, 0, 0, 0, DateTimeKind.Utc), "Aprenda os fundamentos da meditação mindfulness e como ela pode melhorar sua saúde mental e bem-estar diário.", 10, "Introdução à Meditação Mindfulness", null },
                    { new Guid("d4e5f6a7-b8c9-0123-defa-234567890123"), true, new DateTime(2025, 1, 1, 0, 0, 0, 0, DateTimeKind.Utc), "Exercicio", new DateTime(2025, 1, 1, 0, 0, 0, 0, DateTimeKind.Utc), "Técnica de respiração comprovada para reduzir ansiedade: inspire por 4 segundos, segure por 7, expire por 8.", 5, "Respiração 4-7-8 para Ansiedade", null },
                    { new Guid("e5f6a7b8-c9d0-1234-efab-345678901234"), true, new DateTime(2025, 1, 1, 0, 0, 0, 0, DateTimeKind.Utc), "Dica", new DateTime(2025, 1, 1, 0, 0, 0, 0, DateTimeKind.Utc), "Rotinas e hábitos simples que podem transformar a qualidade do seu sono e impactar positivamente sua saúde mental.", 7, "5 Dicas para Melhorar o Sono", null }
                });

            migrationBuilder.CreateIndex(
                name: "IX_meditation_sessions_user_id",
                table: "meditation_sessions",
                column: "user_id");

            migrationBuilder.CreateIndex(
                name: "IX_mood_entries_user_id",
                table: "mood_entries",
                column: "user_id");

            migrationBuilder.CreateIndex(
                name: "IX_users_email",
                table: "users",
                column: "email",
                unique: true);
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropTable(
                name: "meditation_sessions");

            migrationBuilder.DropTable(
                name: "mood_entries");

            migrationBuilder.DropTable(
                name: "wellness_contents");

            migrationBuilder.DropTable(
                name: "users");
        }
    }
}
