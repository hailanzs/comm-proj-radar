import numpy as np
import scipy


### start helper functions ###

def beamform(X,idx):
    """ X is of shape # frames x # Rx x # Tx x # bins 
    """
    ph_bf = 0
    beat_freq = scipy.fft.fft(X, axis=3)
    num_frms, tx, rx, N_range = beat_freq.shape

    idxs = np.arange(idx-2,idx+3)
    
    N_x_stp = rx
    N_z_stp = tx
    theta_s, theta_e = 70, 110
    theta_s *= (np.pi/180)
    theta_e *= (np.pi/180)
    theta_rad_lim = [theta_s,theta_e]
    d_theta = 2/180*np.pi
    phi_s, phi_e = 70, 110
    phi_s *= (np.pi/180)
    phi_e *= (np.pi/180)
    phi_rad_lim = [phi_s,phi_e]
    d_phi = 5/180*np.pi
    theta = np.arange(theta_rad_lim[0],theta_rad_lim[1],d_theta)
    N_theta = len(theta)
    phi = np.arange(phi_rad_lim[0],phi_rad_lim[1],d_phi)
    N_phi = len(phi)
    
    lm = 3e8/77e9
    sph_pwr = np.zeros((num_frms, N_theta, N_phi, 5), dtype=complex)
    sph_pwr_range = np.zeros((N_theta, N_phi, N_range), dtype=complex)
    
    x_idx = np.array([[0.,1.,2.,3.],[-2.,-1.,0.,1.]])
    z_idx = np.array([[0.,0.,0.,0.],[1.,1.,1.,1.]])
    s = lm / 2
    for kt in range(N_theta):
        for kp in range(N_phi):
       
            cos_theta = np.cos(theta[kt])
            sin_theta = np.sin(theta[kt])
            sin_phi = np.sin(phi[kp])
            
            sinp_cost = sin_phi * cos_theta
            sinp_sint = sin_phi * sin_theta
            
            # cos_theta = np.cos(theta[ka])
        
            Vec = np.exp(-1j*(2*np.pi*(s*z_idx*sinp_cost + s*x_idx*sinp_sint)/lm))
            VecRF = np.repeat(Vec[np.newaxis,:,:],num_frms,axis=0)
            VecRFR = np.repeat(VecRF[:,:,:,np.newaxis],N_range,axis=3)
            VecRFI = np.repeat(VecRF[:,:,:,np.newaxis],5,axis=3)
            sph_pwr[:,kt,kp,:] = np.squeeze(np.sum(np.multiply(beat_freq[:,:,:,idxs],VecRFI),axis=(1,2)))
            sph_pwr_range[kt,kp,:] = np.squeeze(np.sum(np.multiply(beat_freq,VecRFR),axis=(0,1,2)))
    
    pwr = np.squeeze(np.mean(abs(sph_pwr[:,:,:,2]),axis=0))**2
    max_loc = np.unravel_index(pwr.argmax(), pwr.shape)
    
    ph_bf = np.unwrap(np.angle(np.squeeze(sph_pwr[:,max_loc[0], max_loc[1],:])), axis=0)
    ph_bf = ph_bf - np.mean(ph_bf,axis=0)
    
    return sph_pwr[:,max_loc[0], max_loc[1],:], ph_bf, sph_pwr_range[max_loc[0], max_loc[1],:]
    
### end helper functions ###


def process_raw_data(X):
    """pre-process raw mm-wave data to get the frequency spectrum."""
    # bring the data to 0 mean
    X_ = np.mean(X, axis=(1,2), keepdims=False)
    X_ = X_ - np.mean(X_, axis=-1, keepdims=True)

    # take range FFT
    X_rfft = scipy.fft.fft(X_, axis=-1)
    # X_bf, X_ph_bf, X_sph_pwr_range = beamform(X, idx)
    X_power = np.abs(np.sum(X,axis=0))
    X_phase_all = np.unwrap(np.angle(X_rfft), axis=0)
    X_phase_all -= np.mean(X_phase_all, axis=0, keepdims=True)
      
    return {'phase': X_phase_all, 'power': X_power}

