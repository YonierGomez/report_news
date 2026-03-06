---
inclusion: always
---

# Flujo de trabajo con Git

Reglas obligatorias para este repositorio:

1. Nunca hacer push directo a `master`. Siempre crear una rama, subir por PR y mergear.

2. Al mergear un PR, SIEMPRE usar `--delete-branch` para borrar la rama remota automáticamente:
   ```bash
   gh pr merge <N> --repo YonierGomez/report_news --merge --delete-branch
   ```

3. Si por alguna razón la rama remota sigue después del merge, borrarla manualmente:
   ```bash
   git push origin --delete <rama>
   ```

4. Después del merge, limpiar las ramas locales:
   ```bash
   git checkout master && git pull
   git branch -d <rama-local>
   ```

5. Regla absoluta: nunca dejar ramas remotas huérfanas después de un merge.

6. Después de mergear cambios de código (scrapers, bot, formatter), SIEMPRE lanzar el workflow con force_build:
   ```bash
   gh workflow run docker-multi-arch.yml --repo YonierGomez/report_news -f force_build=true
   ```
