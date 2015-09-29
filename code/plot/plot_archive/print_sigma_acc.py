import numpy as np

for i in range(1,17):
    ws_lh = np.load('/fastscratch/pohsuan/pHA/data/working/2203TR/pHA_EM_lh_1300vx_'+str(i)+'.npz')
    ws_rh = np.load('/fastscratch/pohsuan/pHA/data/working/2203TR/pHA_EM_rh_1300vx_'+str(i)+'.npz')
    ws_acc= np.load('/fastscratch/pohsuan/pHA/data/working/2203TR/acc_pHA_EM_1300vx_'+str(i)+'.npz')
    print i
    print 'sigma lh'
    print ws_lh['sigma2']
    print 'sigma rh'
    print ws_rh['sigma2']
    print 'average sigma'
    print (ws_lh['sigma2']+ws_rh['sigma2'])/2
    print 'accu'
    print ws_acc['accu']
    print np.mean(ws_acc['accu'])
