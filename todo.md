[X] - Usar Workes/Jobs/Multhreads
[ ] - Traduzir transcripts
[ ] - Refatorar código
    [ ] - Remover processamento e lógicas diretos da requisição. Criar metodos e funcoes


✅ Resumo final

✔ Não execute Whisper dentro do request
✔ Não use threading dentro das classes
✔ Sim, background task no Flask (temporário)
✔ Ideal: Celery / RQ
✔ Encapsule melhor Transcript
✔ Não compartilhe WhisperModel globalmente

Use fila de tarefas

Celery / RQ / Dramatiq

Arquitetura correta
Flask (API)
   |
   |--> cria job (video_id)
        |
        v
Worker (processo separado)
   - yt_dlp
   - Whisper
   - MongoDB