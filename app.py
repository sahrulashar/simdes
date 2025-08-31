from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  

from routes.landing import landing_bp
from routes.aparat import aparat_bp
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.kartu_keluarga import kk_bp
from routes.penduduk import penduduk_bp
from routes.kelahiran import kelahiran_bp
from routes.kematian import kematian_bp
from routes.kepindahan import kepindahan_bp
from routes.pendatang import pendatang_bp
from routes.potensi import potensi_bp
from routes.galeri import galeri_bp
from routes.berita import berita_bp
from routes.sktm import sktm_bp
from routes.user_sktm import user_sktm_bp
from routes.sku import sku_bp
from routes.user_sku import user_sku_bp
from routes.belum_nikah import belum_nikah_bp
from routes.user_belum_menikah import user_belum_nikah_bp
from routes.hilang import hilang_bp
from routes.user_hilang import user_hilang_bp
from routes.keramaian import keramaian_bp
from routes.user_keramaian import user_keramaian_bp
from routes.skm import skm_bp
from routes.user_skm import user_skm_bp
from routes.merantau import merantau_bp
from routes.user_merantau import user_merantau_bp
from routes.cerai import cerai_bp
from routes.user_cerai import user_cerai_bp 
from routes.izin_potong import izin_potong_bp 
from routes.user_izin_potong import user_izin_potong_bp 
from routes.s_kematian import s_kematian_bp 
from routes.user_s_kematian import user_s_kematian_bp 
from routes.s_penguburan import s_penguburan_bp
from routes.user_s_penguburan import user_s_penguburan_bp

app.register_blueprint(landing_bp)
app.register_blueprint(aparat_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(kk_bp)
app.register_blueprint(penduduk_bp)
app.register_blueprint(kelahiran_bp)
app.register_blueprint(kematian_bp)
app.register_blueprint(kepindahan_bp)
app.register_blueprint(pendatang_bp)
app.register_blueprint(potensi_bp)
app.register_blueprint(galeri_bp)
app.register_blueprint(berita_bp)
app.register_blueprint(sktm_bp)
app.register_blueprint(user_sktm_bp)
app.register_blueprint(sku_bp)
app.register_blueprint(user_sku_bp)
app.register_blueprint(belum_nikah_bp)
app.register_blueprint(user_belum_nikah_bp)
app.register_blueprint(hilang_bp)
app.register_blueprint(user_hilang_bp)
app.register_blueprint(keramaian_bp)
app.register_blueprint(user_keramaian_bp)
app.register_blueprint(skm_bp)
app.register_blueprint(user_skm_bp)
app.register_blueprint(merantau_bp)
app.register_blueprint(user_merantau_bp)
app.register_blueprint(cerai_bp)
app.register_blueprint(user_cerai_bp)
app.register_blueprint(izin_potong_bp)
app.register_blueprint(user_izin_potong_bp)
app.register_blueprint(s_kematian_bp)
app.register_blueprint(user_s_kematian_bp)
app.register_blueprint(s_penguburan_bp)
app.register_blueprint(user_s_penguburan_bp)

if __name__ == '__main__':
    app.run(debug=True)
