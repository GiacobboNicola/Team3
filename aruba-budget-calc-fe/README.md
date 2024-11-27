# ABC Frontend

Il `abc-fe` è un prototipo front-end sviluppato con Svelte 5 e SvelteKit. È progettato per assistere i clienti di Aruba nel calcolo dei budget per i loro progetti basati sul cloud, permettendo di configurare risorse come container, cloud computing, storage e networking, fornendo anche informazioni dettagliate sui prezzi.

Idealmente, in una fase più avanzata, l'applicazione consentirà agli utenti di passare senza interruzioni dalla configurazione e preventivazione all'effettivo ordine, semplificando il processo dalla pianificazione all'acquisto.

## Struttura delle Directory

- **src/**
  - **lib/**
    - **components/**: Contiene componenti Svelte riutilizzabili come pulsanti, form e selettori di risorse.
    - **stores/**: Contiene gli store Svelte per gestire lo stato dell'applicazione, inclusi nomi utente e progetti, elementi del carrello e stati di creazione delle risorse.
    - **utils/**: Contiene funzioni di utilità per calcoli ed elaborazione dati.
  - **routes/**: Contiene pagine Svelte e layout per le diverse viste dell'applicazione.
  - **catalogs/**: Contiene file JSON con dati predefiniti delle risorse e informazioni sui prezzi.
  - **types.ts**: Definisce i tipi TypeScript ed enum utilizzati in tutta l'applicazione.

## Flusso dell'Applicazione

1. **Autenticazione Utente**: Gli utenti iniziano dalla pagina principale dove possono accedere.
   Il login è attualmente simulato, in futuro sarà gestito tramite chiamata API e fornirà informazioni essenziali come il Tier dell'utente e il Token necessario per effettuare ordini.
2. **Creazione Progetto**: Questo passaggio è necessario per associare le risorse acquistate a un progetto, in futuro sarà possibile selezionare un progetto precedentemente creato dall'utente.
3. **Selezione Risorse**: Gli utenti possono selezionare un tipo di risorsa e procedere alla sua configurazione.
4. **Configurazione**: Gli utenti configurano la risorsa selezionata specificando opzioni tecniche (disponibili solo per unità di calcolo e container), quantità e dettagli della prenotazione.
5. **Gestione Carrello**: Gli utenti possono visualizzare il loro carrello, che mostra le risorse selezionate e le opzioni scelte. Possono aggiungere nuove risorse o procedere al checkout.
6. **Calcolo Prezzi**: L'applicazione calcola e visualizza i prezzi basati sulle selezioni e configurazioni dell'utente.

## Flusso dei Dati

- **Gestione dello Stato**: L'applicazione utilizza gli store Svelte per gestire lo stato tra i componenti. Ad esempio, lo store `resourceCreation` mantiene il passaggio corrente e la risorsa selezionata, mentre lo store `cart` gestisce gli elementi aggiunti al carrello.
- **Store Derivati**: L'applicazione utilizza store derivati per calcolare valori basati su altri store, come i costi totali basati sugli elementi nel carrello.
- **Gestione Eventi**: I componenti gestiscono le interazioni dell'utente attraverso gestori di eventi, aggiornando lo stato negli store quando necessario.

## Prezzi in Tempo Reale e Configurazione: Dal Prototipo al Prodotto

L'uso di file statici per gestire questo prototipo è una soluzione temporanea necessaria per garantire che le funzionalità core operino efficacemente a scopo dimostrativo. In una fase futura dello sviluppo del prodotto, l'intero flusso di lavoro sarà integrato attraverso chiamate API a servizi backend dedicati. Questi servizi permetteranno una configurazione dinamica delle risorse, come determinare quali opzioni RAM sono compatibili con una CPU selezionata, prevenendo combinazioni non valide e calcolando le percentuali di sconto applicabili basate sulla configurazione dell'utente e sul suo Tier (determinato al login).

Una volta che il frontend e i microservizi backend comunicheranno come previsto nell'architettura, i prezzi delle risorse saranno calcolati dinamicamente in tempo reale in base alla configurazione selezionata. Durante il processo di configurazione, gli utenti potranno vedere i prezzi aggiornarsi istantaneamente mentre modificano le loro scelte.

Lo scopo di questo calcolatore è guidare gli utenti attraverso il processo di progettazione della loro infrastruttura cloud desiderata, offrendo un'esperienza interattiva che privilegia l'intuitività e la facilità d'uso. Una volta completata la configurazione delle risorse del progetto, gli utenti avranno l'opzione di finalizzare il loro acquisto. Questa funzionalità potrà essere completamente implementata quando il FE comunicherà perfettamente con il BE, assicurando che i calcoli dei prezzi siano accurati e riflettano tutte le variabili pertinenti.

### Come usarlo

To start the project simply run

```bash
npm install

npm run dev

# or start the server and open the app in a new browser tab
npm run dev -- --open
```

## Building

To create a production version of your app:

```bash
npm run build
```

You can preview the production build with `npm run preview`.

## More Information

For more details about the project, please refer to the [OVERVIEW.md](OVERVIEW.md) file.

