import streamlit as st
from PIL import Image


hide_streamlit_style = '''
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
'''
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.title('About')
image = Image.open('banner.png')
st.image(image)
st.subheader('Tools Online | Wannaz')
st.write('''
Sebuah tools online yang terbuat dari python, tools ini masih dalam pengembangan,
Tools ini menggunakan ada yang menggunakan APi maupun yang tidak menggunakan APi,
Dibuat dengan python dengan framework Streamlit dan library seperti pandas, numpy, dll,
Akan ada update atau versi setiap bulan bahkan kurang dari satu bulan.
''')
st.subheader('Tentang Lainya')
st.write('**Menu Tools Online** : ')
list_menu = '<ul><li>DA PA Checker</li><li>Auto Wordpress Install</li><li>XMLRPC Result Check Login</li><li>Range IP Address</li><li>Grab Domain siterankdata.com</li><li>WordPress Install Checker</li><li>WordPress Setup Config Checker</li><li>Website Status Code</li><li>Grab Domain in CubDomain.com</li><li>Domain to IP Address</li><li>Grab Domain WP by Theme</li><li>Grab Domain WP by Plugin</li><li>Grab Recent IP Address</li></ul>'
st.markdown(list_menu, unsafe_allow_html=True)
st.write('**Ketentuan Tools**  :')
st.write('Tools ini gratis tidak memakan biaya sama sekali, kami tidak bertanggung jawab atas tindakan user, tools ini tidak menyimpan result atau hasil kalian karena setiap result akan langsung terhapus dalam waktu 30 detik, Anti Logger dan Still Update Tools ~')
st.subheader('Developer')
images = Image.open('rn.jpg')
st.image(images,width=250)
st.write('**Ridwan N** | Coder Wibu | Penggiat IT')
st.subheader('Updates 2.0')
list_update = '''
<ul>
<li>Range IP > Perubahan result range lebih nyaman</li>
<li>Cub Domain Grabber</li>
<li>Domain to IP Address</li>
<li>Grab Domain WP by Theme</li>
<li>Grab Domain WP by Plugin</li>
<li>Grab Recent IP Address</li>
</ul>
'''
st.markdown(list_update,unsafe_allow_html=True)
st.subheader('Lapor Bug / Error')
st.write('Jika kalian mengalami error atau sebuah bug bisa langsung lapor ke link berikut atau ke menu.')
report_bug = '''
<ul>
<li><a href='wa.me/6281328303820'>WhatsApp</a></li>
<li><a href='https://instagram.com/wannaz_id?igshid=YmMyMTA2M2Y='>Instagram</a></li>
</ul>
'''
st.markdown(report_bug,unsafe_allow_html=True)
