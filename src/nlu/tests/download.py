from gliner import GLiNER
model = GLiNER.from_pretrained("gliner-community/gliner_medium-v2.5")
model.save_pretrained("gliner_25_Med")