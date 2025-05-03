import { HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { catchError, switchMap, throwError } from 'rxjs';

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const httpClient = inject(HttpClient);
  const token = localStorage.getItem('access_token');

  if (token) {
    const cloned = req.clone({
      setHeaders: {
        Authorization: `Bearer ${token}`,
      },
    });

    return next(cloned).pipe(
      catchError((error) => {
        if (error.status === 401 && !req.url.includes('/auth/token/refresh/')) {
          const refreshToken = localStorage.getItem('refresh_token');
          if (refreshToken) {
            return httpClient
              .post<{ access: string }>('http://127.0.0.1:8008/api/auth/token/refresh/', {
                refresh: refreshToken,
              })
              .pipe(
                switchMap((tokens) => {
                  localStorage.setItem('access_token', tokens.access);
                  const retryReq = req.clone({
                    setHeaders: {
                      Authorization: `Bearer ${tokens.access}`,
                    },
                  });
                  return next(retryReq);
                }),
                catchError(() => {
                  localStorage.removeItem('access_token');
                  localStorage.removeItem('refresh_token');
                  window.location.href = '/login';
                  return throwError(() => error);
                })
              );
          }
        }
        return throwError(() => error);
      })
    );
  }

  return next(req);
};