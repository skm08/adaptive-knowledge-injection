adaptive-knowledge-injection/
│
├── checkpoints/
│
├── configs/
│   ├── datasets.yaml
│   ├── models.yaml
│   ├── retrieval.yaml
│   ├── training.yaml
│   ├── evaluation.yaml
│   └── preprocessing.yaml
│
├── data/
│   ├── raw/
│   ├── interim/
│   ├── processed/
│   └── splits/
│
├── docs/
│   ├── PROJECT_STATUS.md
│   ├── TODO.md
│   ├── DESIGN_DECISIONS.md
│   ├── REPOSITORY_MAP.md
│   ├── CODING_STANDARD.md
│   ├── EXPERIMENTS.md
│   ├── CHANGELOG.md
│   ├── PROMPTS.md
│   └── PAPER_PLAN.md
│
├── notebooks/
│   ├── 01_environment.ipynb
│   ├── 02_prepare_data.ipynb
│   ├── 03_build_rag.ipynb
│   ├── 04_train_peft.ipynb
│   ├── 05_build_hybrid.ipynb
│   ├── 06_run_experiments.ipynb
│   └── 07_analysis.ipynb
│
├── outputs/
│   ├── logs/
│   ├── figures/
│   ├── tables/
│   ├── predictions/
│   └── reports/
│
├── scripts/
│
├── src/
│   ├── datasets/
│   │   ├── downloader.py
│   │   ├── loader.py
│   │   └── validator.py
│   │
│   ├── preprocessing/
│   │   ├── cleaner.py
│   │   ├── splitter.py
│   │   └── schema.py
│   │
│   ├── retrieval/
│   │   ├── retriever.py
│   │   ├── vector_store.py
│   │   └── chunking.py
│   │
│   ├── models/
│   │   ├── base_model.py
│   │   ├── rag.py
│   │   ├── peft.py
│   │   └── hybrid.py
│   │
│   ├── evaluation/
│   │   ├── metrics.py
│   │   ├── hallucination.py
│   │   └── statistics.py
│   │
│   ├── experiments/
│   │   ├── run_rag.py
│   │   ├── run_peft.py
│   │   ├── run_hybrid.py
│   │   └── run_full_benchmark.py
│   │
│   └── utils/
│       ├── config.py
│       ├── io.py
│       ├── logger.py
│       ├── seed.py
│       └── constants.py
│
├── tests/
│
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
└── environment.yml