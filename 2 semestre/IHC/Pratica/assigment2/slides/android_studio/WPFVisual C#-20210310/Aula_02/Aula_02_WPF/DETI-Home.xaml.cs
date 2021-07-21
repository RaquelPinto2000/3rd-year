using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace Aula_02_WPF
{
    /// <summary>
    /// Interaction logic for DETI_Home.xaml
    /// </summary>
    public partial class DETI_Home : Page
    {
        public DETI_Home()
        {
            InitializeComponent();
        }

        public void On_Click()
        {

            if (cursosListBox.SelectedValue != null)
            {
                DETI_Cursos cursosPage = new DETI_Cursos();
                this.NavigationService.Navigate(cursosPage);
                cursosPage.labelNome.Content = ((ListBoxItem)cursosListBox.SelectedValue).Content.ToString();
            }
            else
                MessageBox.Show("Selecione um curso", "Erro", MessageBoxButton.OK);
        }

        private void Button_Click(object sender, RoutedEventArgs e)
        {
            On_Click();
        }

        private void ListBoxItem_MouseDoubleClick(object sender, MouseButtonEventArgs e)
        {
            On_Click();
        }
    }
}
