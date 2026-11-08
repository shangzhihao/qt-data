# qt-data

Toy knowledge base for the quality-tracking prototype (plays the role of
vws-data). `kb.json` holds a knowledge quality per topic; `qt-graph` reads it
through `QT_COMPONENT_DATA_PATH`. Lowering a value makes answers on that topic
fail more often, which is how a data regression is simulated.

Changes to this README do not affect quality; they still create a new state.
